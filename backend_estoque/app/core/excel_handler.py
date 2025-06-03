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
    if not EXCEL_FILE_PATH.exists():
        try:
            engine = get_excel_writer_engine()
            with pd.ExcelWriter(EXCEL_FILE_PATH, engine=engine) as writer:
                pd.DataFrame(columns=STOCK_COLUMNS).to_excel(writer, sheet_name=STOCK_SHEET_NAME, index=False)
                pd.DataFrame(columns=TRANSACTION_COLUMNS).to_excel(writer, sheet_name=TRANSACTIONS_SHEET_NAME, index=False)
            print(f"Arquivo Excel '{EXCEL_FILE_PATH}' criado com sucesso.")
        except Exception as e:
            print(f"Erro ao criar arquivo Excel: {e}")
            raise

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
    """Escreve um DataFrame para uma planilha, substituindo o conteúdo existente."""
    initialize_excel()
    engine = get_excel_writer_engine()
    try:
        with pd.ExcelWriter(EXCEL_FILE_PATH, engine=engine, mode='r+') as writer:
            all_sheets = pd.read_excel(EXCEL_FILE_PATH, sheet_name=None, engine='openpyxl')
            all_sheets[sheet_name] = df

            # Re-escreve o arquivo inteiro
        with pd.ExcelWriter(EXCEL_FILE_PATH, engine=engine) as writer_new:
            for s_name, s_df in all_sheets.items():
                s_df.to_excel(writer_new, sheet_name=s_name, index=False)

    except FileNotFoundError:
         with pd.ExcelWriter(EXCEL_FILE_PATH, engine=engine) as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    except Exception as e:
        print(f"Erro ao escrever na planilha '{sheet_name}': {e}")


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

def generate_product_id(nome_produto: str, tipo_produto: str) -> str:
    """Gera um ID de produto único (exemplo simples)."""
    return f"{nome_produto.strip().replace(' ', '_')}_{tipo_produto.strip().replace(' ', '_')}".lower()