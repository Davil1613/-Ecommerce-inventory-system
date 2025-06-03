# 📦 Sistema de Gestão de Estoque Dinâmico

Sistema para gerenciamento de estoque desenvolvido com **Python (FastAPI)** para o backend e **Next.js** para o frontend. Focado em automatizar o registro de entradas e saídas de produtos, com armazenamento persistente em arquivos Excel e visualização de dados através de gráficos interativos.

---

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

---

## 📂 Estrutura Básica do Projeto
Com certeza! Baseado no estilo do README do "Lev Robots Node" que você compartilhou e no projeto de gestão de estoque que estamos desenvolvendo, aqui está uma sugestão de README para o seu sistema:

Markdown

# 📦 Sistema de Gestão de Estoque Dinâmico

Sistema para gerenciamento de estoque desenvolvido com **Python (FastAPI)** para o backend e **Next.js** para o frontend. Focado em automatizar o registro de entradas e saídas de produtos, com armazenamento persistente em arquivos Excel e visualização de dados através de gráficos interativos.

---

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

---

## 📂 Estrutura Básica do Projeto

Estrutura do Backend (backend_estoque/)
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
