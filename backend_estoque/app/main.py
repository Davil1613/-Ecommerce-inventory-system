from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import inventory_router
from app.core.excel_handler import initialize_excel

# Inicializa o arquivo Excel se não existir (bom fazer no início)
try:
    initialize_excel()
except Exception as e:
    print(f"CRÍTICO: Não foi possível inicializar o arquivo Excel. A aplicação pode não funcionar corretamente. Erro: {e}")


app = FastAPI(
    title="API de Gestão de Estoque",
    description="API para gerenciar entrada, saída e consulta de produtos em estoque usando Excel.",
    version="0.1.0"
)

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui o router de inventário
app.include_router(inventory_router.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API de Gestão de Estoque!"}

# Para rodar a aplicação (coloque isso em um if __name__ == "__main__" se for executar este arquivo diretamente)
# ou use o comando uvicorn: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Exemplo para rodar com uvicorn diretamente (opcional):
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)