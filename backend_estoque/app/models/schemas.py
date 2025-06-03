from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

class ProductBase(BaseModel):
    NomeProduto: str
    ValorUnitario: float = Field(gt=0)

class ProductStock(ProductBase):
    ID_Produto: int
    Quantidade: int
    DataUltimaAtualizacao: date

class StockMovement(BaseModel):
    NomeProduto: str
    Quantidade: int = Field(gt=0)
    ValorUnitario: Optional[float] = None 
    DataMovimentacao: date = Field(default_factory=date.today)

class TransactionRecord(BaseModel):
    ID_Transacao: int
    DataHora: date
    ID_Produto: int
    NomeProduto: str
    TipoMovimentacao: str
    Quantidade: int
    ValorTotalMovimentacao: float

class StockResponse(BaseModel):
    message: str
    data: Optional[ProductStock | List[ProductStock] | TransactionRecord | List[TransactionRecord]] = None