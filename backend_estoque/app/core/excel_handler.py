import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from app.core.config import EXCEL_FILE_PATH, STOCK_SHEET_NAME, TRANSACTIONS_SHEET_NAME, STOCK_COLUMNS, TRANSACTION_COLUMNS
import os

def get_excel_writer_engine():
    try:
        import xlsxwriter
        return 'xlsxwriter'
    except ImportError:
        return 'openpyxl'

def initialize_excel():
    file_exists = EXCEL_FILE_PATH.exists()
    # Se o arquivo não existe ou está vazio, (re)cria com cabeçalhos
    if not file_exists or os.path.getsize(EXCEL_FILE_PATH) == 0:
        try:
            print(f"Inicializando arquivo Excel '{EXCEL_FILE_PATH}' com planilhas e cabeçalhos.")
            engine = get_excel_writer_engine()
            with pd.ExcelWriter(EXCEL_FILE_PATH, engine=engine) as writer:
                pd.DataFrame(columns=STOCK_COLUMNS).to_excel(writer, sheet_name=STOCK_SHEET_NAME, index=False)
                pd.DataFrame(columns=TRANSACTION_COLUMNS).to_excel(writer, sheet_name=TRANSACTIONS_SHEET_NAME, index=False)
        except Exception as e:
            print(f"ERRO CRÍTICO ao inicializar arquivo Excel: {e}")
            raise # Importante relançar para sinalizar falha na inicialização
        return

    # Se o arquivo existe, verifica se as planilhas estão lá
    try:
        with pd.ExcelFile(EXCEL_FILE_PATH, engine='openpyxl') as xls:
            existing_sheets = xls.sheet_names

        sheets_to_add = {}
        if STOCK_SHEET_NAME not in existing_sheets:
            sheets_to_add[STOCK_SHEET_NAME] = STOCK_COLUMNS
        if TRANSACTIONS_SHEET_NAME not in existing_sheets:
            sheets_to_add[TRANSACTIONS_SHEET_NAME] = TRANSACTION_COLUMNS

        if sheets_to_add:
            print(f"Adicionando planilhas ausentes: {list(sheets_to_add.keys())}")
            # Ler dados existentes para não perdê-los
            all_data = {sheet: pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet, engine='openpyxl') for sheet in existing_sheets}

            for sheet_name, columns in sheets_to_add.items():
                all_data[sheet_name] = pd.DataFrame(columns=columns) # Cria a nova planilha vazia com colunas

            engine = get_excel_writer_engine()
            with pd.ExcelWriter(EXCEL_FILE_PATH, engine=engine) as writer:
                for s_name, s_df in all_data.items():
                    s_df.to_excel(writer, sheet_name=s_name, index=False)
    except Exception as e:
        print(f"AVISO: Problema ao verificar/adicionar planilhas em arquivo existente: {e}. Pode ser necessário apagar o arquivo Excel e reiniciar.")

def read_sheet(sheet_name: str) -> pd.DataFrame:
    initialize_excel() # Garante que o arquivo e a planilha existam
    try:
        return pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name, engine='openpyxl')
    except FileNotFoundError:
        print(f"Arquivo Excel não encontrado em: {EXCEL_FILE_PATH}")
        return pd.DataFrame() # Retorna DataFrame vazio se não encontrar
    except ValueError as e: # Planilha não encontrada
        print(f"Erro ao ler planilha '{sheet_name}': {e}. Verifique se a planilha existe.")

        if sheet_name == STOCK_SHEET_NAME:
            return pd.DataFrame(columns=STOCK_COLUMNS)
        elif sheet_name == TRANSACTIONS_SHEET_NAME:
            return pd.DataFrame(columns=TRANSACTION_COLUMNS)
        return pd.DataFrame()


def write_df_to_excel(df: pd.DataFrame, sheet_name: str):
    initialize_excel()

    # Converter colunas de data para timezone-naive ANTES de escrever
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            # Se a coluna for de data e tiver fuso horário, remova-o
            if df[col].dt.tz is not None:
                print(f"Convertendo coluna '{col}' da planilha '{sheet_name}' para timezone-naive.")
                df[col] = df[col].dt.tz_localize(None)

    engine = get_excel_writer_engine()
    try:
        # Lógica para ler todas as planilhas existentes e reescrever (para não perder outras planilhas)
        all_sheets = {}
        if EXCEL_FILE_PATH.exists() and os.path.getsize(EXCEL_FILE_PATH) > 0:
            try:
                with pd.ExcelFile(EXCEL_FILE_PATH, engine='openpyxl') as xls:
                    all_sheets = {s_name: xls.parse(s_name) for s_name in xls.sheet_names}
            except Exception as e_read:
                print(f"Aviso: Não foi possível ler o arquivo Excel existente: {e_read}. Ele pode ser alterado.")

        all_sheets[sheet_name] = df # Adiciona ou substitui a planilha atualizada

        with pd.ExcelWriter(EXCEL_FILE_PATH, engine=engine) as writer:
            for s_name, s_df_to_write in all_sheets.items():
                s_df_to_write.to_excel(writer, sheet_name=s_name, index=False)
        # print(f"Planilha '{sheet_name}' escrita com sucesso em '{EXCEL_FILE_PATH}'.")

    except Exception as e:
        print(f"erro ao editar base '{sheet_name}': {e}") # Mantido para depuração
        raise # Re-levanta a exceção para que a camada de serviço possa tratá-la

def append_to_sheet(data_dict: Dict[str, Any], sheet_name: str):
    """Adiciona uma nova linha a uma planilha existente."""
    initialize_excel()
    df_sheet = read_sheet(sheet_name)
    
    # Garante que o DataFrame tenha as colunas corretas se estiver vazio
    expected_columns = TRANSACTION_COLUMNS if sheet_name == TRANSACTIONS_SHEET_NAME else STOCK_COLUMNS
    if df_sheet.empty and not all(col in df_sheet.columns for col in expected_columns):
        df_sheet = pd.DataFrame(columns=expected_columns)

    new_row_df = pd.DataFrame([data_dict])
    df_updated = pd.concat([df_sheet, new_row_df], ignore_index=True)
    write_df_to_excel(df_updated, sheet_name)

def get_next_transaction_id() -> int:
    """Obtém o próximo ID de transação sequencial."""
    df_transactions = read_sheet(TRANSACTIONS_SHEET_NAME)
    if df_transactions.empty or 'ID_Transacao' not in df_transactions.columns:
        return 1
    return df_transactions['ID_Transacao'].max() + 1 if not df_transactions['ID_Transacao'].empty else 1

def generate_product_id(nome_produto: str) -> str:
    """Gera um ID de produto único (exemplo simples)."""
    return f"{nome_produto.strip().replace(' ', '_')}".lower()