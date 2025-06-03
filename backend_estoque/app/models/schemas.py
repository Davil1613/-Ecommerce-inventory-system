from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    NomeProduto: str
    TipoProduto: str
    ValorUnitario: float = Field(gt=0)
class ProductCreate(ProductBase):
    Quantidade: int = Field(gt=0)
    DataRecebimento: datetime = Field(default_factory=datetime.now)

class ProductStock(ProductBase):
    ID_Produto: str
    Quantidade: int
    DataUltimaAtualizacao: datetime

class StockMovement(BaseModel):
    ID_Produto: Optional[str] = None
    NomeProduto: str
    TipoProduto: str
    Quantidade: int = Field(gt=0)
    ValorUnitario: Optional[float] = None 
    DataMovimentacao: datetime = Field(default_factory=datetime.now)

class TransactionRecord(BaseModel):
    ID_Transacao: int
    DataHora: datetime
    ID_Produto: str
    NomeProduto: str
    TipoProduto: str
    TipoMovimentacao: str
    Quantidade: int
    ValorUnitarioMovimentacao: float
    ValorTotalMovimentacao: float

class StockResponse(BaseModel):
    message: str
    data: Optional[ProductStock | List[ProductStock] | TransactionRecord | List[TransactionRecord]] = None