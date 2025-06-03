import os
from pathlib import Path

# Define o caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Caminho para o arquivo Excel
EXCEL_FILE_PATH = BASE_DIR / "estoque.xlsx"

# Nomes das planilhas
STOCK_SHEET_NAME = "EstoqueAtual"
TRANSACTIONS_SHEET_NAME = "HistoricoTransacoes"

# Colunas esperadas
STOCK_COLUMNS = ["ID_Produto", "NomeProduto", "ValorUnitario", "Quantidade", "DataUltimaAtualizacao", "ValorTotal"]
TRANSACTION_COLUMNS = ["ID_Transacao", "DataHora", "ID_Produto", "NomeProduto", "TipoMovimentacao", "Quantidade", "ValorTotalMovimentacao"]