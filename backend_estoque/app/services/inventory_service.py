from datetime import datetime
from typing import List, Optional
from app.models import schemas
import pandas as pd
from app.core.config import (EXCEL_FILE_PATH, STOCK_SHEET_NAME, TRANSACTIONS_SHEET_NAME, STOCK_COLUMNS)
from app.core.excel_handler import (append_to_sheet, get_next_transaction_id, read_sheet, write_df_to_excel)
from app.models.schemas import (ProductStock, StockMovement, TransactionRecord)


def add_product_entry(movement: schemas.StockMovement) -> schemas.ProductStock:
    df_stock = read_sheet(STOCK_SHEET_NAME)

    # Pré-processamento do DataFrame de estoque para consistência
    if not df_stock.empty:
        for col in ['NomeProduto']: # Coluna usada para identificar o produto
            if col in df_stock.columns:
                df_stock[col] = df_stock[col].astype(str).str.strip() # Garante string e remove espaços extras
        if 'ID_Produto' in df_stock.columns:
            df_stock['ID_Produto'] = pd.to_numeric(df_stock['ID_Produto'], errors='coerce').fillna(0).astype(int)
        else: # Se a coluna ID_Produto não existir (primeira execução em arquivo antigo ou erro)
            df_stock['ID_Produto'] = pd.Series(dtype='int') # Cria coluna vazia do tipo int

    nome_produto_req = movement.NomeProduto.strip()

    existing_product_series = df_stock[
        (df_stock['NomeProduto'].str.lower() == nome_produto_req.lower())
    ]

    product_id: int
    valor_unitario_transacao: float

    if not existing_product_series.empty:
        # Produto existente: Atualiza quantidade e, opcionalmente, valor unitário
        product_id = int(existing_product_series['ID_Produto'].iloc[0])
        idx = existing_product_series.index[0]

        df_stock.loc[idx, 'Quantidade'] += movement.Quantidade
        
        # Atualiza ValorUnitario se um novo valor for fornecido
        if movement.ValorUnitario is not None:
            df_stock.loc[idx, 'ValorUnitario'] = movement.ValorUnitario
            valor_unitario_transacao = movement.ValorUnitario
        else:
            # Se não fornecido, usa o valor unitário existente para a transação
            valor_unitario_transacao = df_stock.loc[idx, 'ValorUnitario']
        df_stock.loc[idx, 'ValorTotal'] = df_stock.loc[idx, 'Quantidade'] * df_stock.loc[idx, 'ValorUnitario']
        df_stock.loc[idx, 'DataUltimaAtualizacao'] = movement.DataMovimentacao
    else:
        # Produto novo: Atribui novo ID_Produto sequencial
        if movement.ValorUnitario is None:
            raise ValueError("ValorUnitario é obrigatório para o primeiro registro de um novo produto.")
        
        valor_unitario_transacao = movement.ValorUnitario

        if df_stock.empty or df_stock['ID_Produto'].isna().all() or df_stock['ID_Produto'].max() == 0:
            product_id = 1
        else:
            max_id = df_stock['ID_Produto'].max() # Assume que ID_Produto é numérico e já tratado
            product_id = int(max_id + 1)
        
        new_stock_item = {
            "ID_Produto": product_id,
            "NomeProduto": nome_produto_req,
            "ValorUnitario": movement.ValorUnitario,
            "Quantidade": movement.Quantidade,
            "DataUltimaAtualizacao": movement.DataMovimentacao,
            "ValorTotal": movement.Quantidade * movement.ValorUnitario
        }
        # Garante que o novo DataFrame tenha as colunas corretas antes de concatenar
        new_stock_df = pd.DataFrame([new_stock_item])
        if not df_stock.empty:
            # Alinha colunas com df_stock existente, preenchendo com NaN se necessário (pouco provável aqui)
            new_stock_df = new_stock_df.reindex(columns=df_stock.columns)
        else:
            # Se df_stock estava vazio, usa STOCK_COLUMNS para definir a ordem e colunas
            new_stock_df = new_stock_df.reindex(columns=STOCK_COLUMNS)


        df_stock = pd.concat([df_stock, new_stock_df], ignore_index=True)

    # Garante que a coluna ID_Produto seja do tipo int antes de salvar
    df_stock['ID_Produto'] = df_stock['ID_Produto'].astype(int)
    write_df_to_excel(df_stock, STOCK_SHEET_NAME)

    # Registra transação
    transaction_data = schemas.TransactionRecord(
        ID_Transacao=get_next_transaction_id(), # Função para pegar o próximo ID da planilha de transações
        DataHora=movement.DataMovimentacao,
        ID_Produto=product_id, # product_id já é int
        NomeProduto=nome_produto_req,
        TipoMovimentacao="ENTRADA",
        Quantidade=movement.Quantidade,
        ValorUnitarioMovimentacao=valor_unitario_transacao,
        ValorTotalMovimentacao=movement.Quantidade * valor_unitario_transacao
    )
    append_to_sheet(transaction_data.model_dump(), TRANSACTIONS_SHEET_NAME)

    # Busca o item de estoque (atualizado ou novo) para retornar na resposta
    # É importante buscar após a concatenação, pois o índice pode ter mudado
    updated_product_info = df_stock[df_stock['ID_Produto'] == product_id].iloc[0]
    return schemas.ProductStock(**updated_product_info.to_dict())

def remove_product_stock(movement: schemas.StockMovement) -> schemas.ProductStock:
    df_stock = read_sheet(STOCK_SHEET_NAME)
    
    # Pré-processamento
    if not df_stock.empty:
        for col in ['NomeProduto']:
            if col in df_stock.columns:
                df_stock[col] = df_stock[col].astype(str).str.strip()
        if 'ID_Produto' in df_stock.columns:
            df_stock['ID_Produto'] = pd.to_numeric(df_stock['ID_Produto'], errors='coerce').fillna(0).astype(int)
        else:
            raise ValueError("Planilha de estoque não contém ID_Produto. Verifique a integridade do arquivo.")

    nome_produto_req = movement.NomeProduto.strip()

    existing_product_series = df_stock[
        (df_stock['NomeProduto'].str.lower() == nome_produto_req.lower()) 
    ]

    if existing_product_series.empty:
        raise ValueError(f"Produto '{nome_produto_req}' não encontrado no estoque.")

    idx = existing_product_series.index[0]
    product_id = int(existing_product_series['ID_Produto'].iloc[0])
    current_quantity = df_stock.loc[idx, 'Quantidade']
    valor_unitario_atual_estoque = df_stock.loc[idx, 'ValorUnitario']

    if current_quantity < movement.Quantidade:
        raise ValueError(f"Quantidade insuficiente em estoque para '{nome_produto_req}'. Disponível: {current_quantity}")

    df_stock.loc[idx, 'Quantidade'] -= movement.Quantidade
    df_stock.loc[idx, 'DataUltimaAtualizacao'] = movement.DataMovimentacao
    df_stock.loc[idx, 'ValorTotal'] = df_stock.loc[idx, 'Quantidade'] * df_stock.loc[idx, 'ValorUnitario']
    
    df_stock['ID_Produto'] = df_stock['ID_Produto'].astype(int) # Garante tipo antes de salvar
    write_df_to_excel(df_stock, STOCK_SHEET_NAME)

    # Registra transação
    transaction_data = schemas.TransactionRecord(
        ID_Transacao=get_next_transaction_id(),
        DataHora=movement.DataMovimentacao,
        ID_Produto=product_id,
        NomeProduto=nome_produto_req,
        TipoMovimentacao="SAIDA",
        Quantidade=movement.Quantidade,
        ValorUnitarioMovimentacao=valor_unitario_atual_estoque, # Usa o valor do estoque no momento da saída
        ValorTotalMovimentacao=movement.Quantidade * valor_unitario_atual_estoque
    )
    append_to_sheet(transaction_data.model_dump(), TRANSACTIONS_SHEET_NAME)
    
    updated_product_info = df_stock[df_stock['ID_Produto'] == product_id].iloc[0]
    return schemas.ProductStock(**updated_product_info.to_dict())

def get_all_stock_items() -> List[ProductStock]:
    # Retorna todos os itens atualmente em estoque
    df_stock = read_sheet(STOCK_SHEET_NAME)
    if df_stock.empty:
        return []
    return [ProductStock(**row.to_dict()) for _, row in df_stock.iterrows()]

def get_transaction_history(start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None,
                            product_type: Optional[str] = None) -> List[TransactionRecord]:
    # Retorna o histórico de transações, com filtros opcionais
    df_transactions = read_sheet(TRANSACTIONS_SHEET_NAME)
    if df_transactions.empty:
        return []

    # Converte DataHora para datetime se não estiver
    if 'DataHora' in df_transactions.columns:
         df_transactions['DataHora'] = pd.to_datetime(df_transactions['DataHora'])


    if start_date:
        df_transactions = df_transactions[df_transactions['DataHora'] >= start_date]
    if end_date:
        # Adiciona 1 dia ao end_date para incluir transações do dia inteiro
        # end_date_inclusive = end_date + timedelta(days=1)
        # df_transactions = df_transactions[df_transactions['DataHora'] < end_date_inclusive]
        # Ou, se DataHora já for datetime, pode comparar diretamente
        df_transactions = df_transactions[df_transactions['DataHora'] <= end_date]

    return [TransactionRecord(**row.to_dict()) for _, row in df_transactions.iterrows()]