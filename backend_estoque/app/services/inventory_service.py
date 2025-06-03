from datetime import datetime
from typing import List, Optional

import pandas as pd
from app.core.config import (EXCEL_FILE_PATH, STOCK_SHEET_NAME,
                             TRANSACTIONS_SHEET_NAME)
from app.core.excel_handler import (append_to_sheet, generate_product_id,
                                    get_next_transaction_id, read_sheet,
                                    write_df_to_excel)
from app.models.schemas import (ProductStock, StockMovement,
                                TransactionRecord)


def add_product_entry(movement: StockMovement) -> ProductStock:
    """Adiciona uma entrada de produto ao estoque e registra a transação."""
    df_stock = read_sheet(STOCK_SHEET_NAME)

    product_id = movement.ID_Produto or generate_product_id(movement.NomeProduto, movement.TipoProduto)
    
    if movement.ValorUnitario is None:
        # Tenta buscar o valor unitário do estoque se já existir
        existing_product_series = df_stock[df_stock['ID_Produto'] == product_id]
        if not existing_product_series.empty:
            movement.ValorUnitario = existing_product_series['ValorUnitario'].iloc[0]
        else:
            raise ValueError("ValorUnitario é obrigatório para o primeiro registro de um produto.")


    # Atualiza ou adiciona no EstoqueAtual
    if product_id in df_stock['ID_Produto'].values:
        idx = df_stock.index[df_stock['ID_Produto'] == product_id][0]
        df_stock.loc[idx, 'Quantidade'] += movement.Quantidade
        df_stock.loc[idx, 'ValorUnitario'] = movement.ValorUnitario # Pode atualizar o valor
        df_stock.loc[idx, 'DataUltimaAtualizacao'] = movement.DataMovimentacao
    else:
        new_stock_item = {
            "ID_Produto": product_id,
            "NomeProduto": movement.NomeProduto,
            "TipoProduto": movement.TipoProduto,
            "ValorUnitario": movement.ValorUnitario,
            "Quantidade": movement.Quantidade,
            "DataUltimaAtualizacao": movement.DataMovimentacao
        }
        new_stock_df = pd.DataFrame([new_stock_item])
        df_stock = pd.concat([df_stock, new_stock_df], ignore_index=True)

    write_df_to_excel(df_stock, STOCK_SHEET_NAME)

    # Registra transação
    transaction_data = TransactionRecord(
        ID_Transacao=get_next_transaction_id(),
        DataHora=movement.DataMovimentacao,
        ID_Produto=product_id,
        NomeProduto=movement.NomeProduto,
        TipoProduto=movement.TipoProduto,
        TipoMovimentacao="ENTRADA",
        Quantidade=movement.Quantidade,
        ValorUnitarioMovimentacao=movement.ValorUnitario,
        ValorTotalMovimentacao=movement.Quantidade * movement.ValorUnitario
    )
    append_to_sheet(transaction_data.model_dump(), TRANSACTIONS_SHEET_NAME)

    updated_product_info = df_stock[df_stock['ID_Produto'] == product_id].iloc[0]
    return ProductStock(**updated_product_info.to_dict())


def remove_product_stock(movement: StockMovement) -> ProductStock:
    """Remove uma quantidade de produto do estoque e registra a transação."""
    df_stock = read_sheet(STOCK_SHEET_NAME)
    product_id = movement.ID_Produto or generate_product_id(movement.NomeProduto, movement.TipoProduto)

    if product_id not in df_stock['ID_Produto'].values:
        raise ValueError(f"Produto com ID '{product_id}' não encontrado no estoque.")

    idx = df_stock.index[df_stock['ID_Produto'] == product_id][0]
    current_quantity = df_stock.loc[idx, 'Quantidade']
    valor_unitario_atual = df_stock.loc[idx, 'ValorUnitario'] # Usar o valor atual do estoque para a saída

    if current_quantity < movement.Quantidade:
        raise ValueError(f"Quantidade insuficiente em estoque para '{product_id}'. Disponível: {current_quantity}")

    df_stock.loc[idx, 'Quantidade'] -= movement.Quantidade
    df_stock.loc[idx, 'DataUltimaAtualizacao'] = movement.DataMovimentacao
    write_df_to_excel(df_stock, STOCK_SHEET_NAME)

    # Registra transação
    transaction_data = TransactionRecord(
        ID_Transacao=get_next_transaction_id(),
        DataHora=movement.DataMovimentacao,
        ID_Produto=product_id,
        NomeProduto=df_stock.loc[idx, 'NomeProduto'],
        TipoProduto=df_stock.loc[idx, 'TipoProduto'],
        TipoMovimentacao="SAIDA",
        Quantidade=movement.Quantidade,
        ValorUnitarioMovimentacao=valor_unitario_atual, # Valor do momento da saida
        ValorTotalMovimentacao=movement.Quantidade * valor_unit_atual
    )
    append_to_sheet(transaction_data.model_dump(), TRANSACTIONS_SHEET_NAME)
    
    updated_product_info = df_stock[df_stock['ID_Produto'] == product_id].iloc[0]
    return ProductStock(**updated_product_info.to_dict())


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
    if product_type:
        df_transactions = df_transactions[df_transactions['TipoProduto'].str.lower() == product_type.lower()]

    return [TransactionRecord(**row.to_dict()) for _, row in df_transactions.iterrows()]