from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from app.models.schemas import StockMovement, ProductStock, TransactionRecord, StockResponse
from app.services import inventory_service

router = APIRouter(
    prefix="/api/inventory",  # Prefixo para todas as rotas neste router
    tags=["Inventory"]       # Agrupa estas rotas na documentação do Swagger/OpenAPI
)

@router.post("/entrada", response_model=StockResponse)
async def registrar_entrada_produto(movement: StockMovement):
    try:
        if movement.ValorUnitario is None or movement.ValorUnitario <= 0:
             # Para entradas, o valor unitário da compra é essencial
             # Se o produto já existe, poderíamos pegar o último valor, mas para uma nova entrada,
             # o valor da compra é importante.
             # No service, já tratamos isso para o caso de ser uma atualização.
             # Mas uma validação inicial aqui pode ser útil.
             pass # Deixe o service validar por enquanto
        
        updated_product = inventory_service.add_product_entry(movement)
        return StockResponse(message="Entrada registrada com sucesso!", data=updated_product)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log a exceção e:
        print(f"Erro inesperado em registrar_entrada_produto: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno no servidor.")


@router.post("/saida", response_model=StockResponse)
async def registrar_saida_produto(movement: StockMovement):
    try:
        updated_product = inventory_service.remove_product_stock(movement)
        return StockResponse(message="Saída registrada com sucesso!", data=updated_product)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Erro inesperado em registrar_saida_produto: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno no servidor.")

@router.get("/estoque", response_model=StockResponse)
async def listar_estoque_atual():
    try:
        stock_items = inventory_service.get_all_stock_items()
        return StockResponse(message="Estoque atual recuperado com sucesso.", data=stock_items)
    except Exception as e:
        print(f"Erro inesperado em listar_estoque_atual: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno ao buscar o estoque.")


@router.get("/transacoes", response_model=StockResponse)
async def listar_historico_transacoes(
    data_inicio: Optional[datetime] = Query(None, description="Data de início do filtro (YYYY-MM-DDTHH:MM:SS)"),
    data_fim: Optional[datetime] = Query(None, description="Data de fim do filtro (YYYY-MM-DDTHH:MM:SS)"),
    tipo_produto: Optional[str] = Query(None, description="Filtrar por tipo de produto")
):
    try:
        transactions = inventory_service.get_transaction_history(
            start_date=data_inicio,
            end_date=data_fim,
            product_type=tipo_produto
        )
        return StockResponse(message="Histórico de transações recuperado com sucesso.", data=transactions)
    except Exception as e:
        print(f"Erro inesperado em listar_historico_transacoes: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno ao buscar transações.")