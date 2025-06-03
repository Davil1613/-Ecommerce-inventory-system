## 🎯 Objetivo do Projeto

Este projeto visa **simplificar e automatizar o controle de inventário**, permitindo:

- Registrar facilmente entradas e saídas de produtos.
- Calcular e atualizar automaticamente o saldo em estoque.
- Armazenar todas as movimentações e o estado atual do estoque em um arquivo Excel.
- Fornecer uma interface web amigável para visualizar dados, aplicar filtros (por data, tipo de produto) e analisar o estoque através de gráficos.
- Facilitar a tomada de decisão com base em dados precisos do inventário.

---

## 🛠️ Tecnologias Utilizadas

- **Backend**:
    - **Python**
    - **FastAPI**: Para a criação da API RESTful.
    - **Pandas**: Para manipulação de dados e interação com arquivos Excel.
    - **Uvicorn**: Como servidor ASGI para rodar a API FastAPI.
    - **Pydantic**: Para validação de dados.
    - `venv`: Para gerenciamento de ambiente virtual Python.
- **Frontend**:
    - **Next.js**: Framework React para a interface do usuário.
    - **TypeScript** (ou JavaScript)
    - **React**
    - **Chart.js** (ou Recharts, Nivo): Para a criação de gráficos.
    - **Axios** (ou Fetch API): Para comunicação com o backend.
- **Armazenamento de Dados**:
    - **Microsoft Excel** (`.xlsx`): Para persistência dos dados de estoque e transações.

## ⚙️ Comandos de Execução
```
npm run back               # Para executar o BACKEND
npm run front              # Para executar o FRONTEND
npm run dev                # Para executar o FRONTEND e BACKEND
```

## ⚙️ link HML backend
ip:8000/docs#/

## 📂 Estrutura Básica do Projeto

Estrutura do Backend (backend_estoque/)
```
backend_estoque/
├── venv/                   # Ambiente virtual Python
├── app/                    # Código principal da aplicação backend
│   ├── init.py
│   ├── core/               # Lógica central, manipulação de Excel, config
│   │   ├── init.py
│   │   ├── config.py
│   │   └── excel_handler.py
│   ├── models/             # Modelos Pydantic para validação
│   │   ├── init.py
│   │   └── schemas.py
│   ├── routers/            # Endpoints da API (FastAPI routers)
│   │   ├── init.py
│   │   └── inventory_router.py
│   ├── services/           # Lógica de negócio
│   │   ├── init.py
│   │   └── inventory_service.py
│   └── main.py             # Ponto de entrada da API FastAPI
│
├── estoque.xlsx            # Arquivo de dados do estoque
└── requirements.txt        # Dependências Python


