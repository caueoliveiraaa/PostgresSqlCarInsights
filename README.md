# Arquitetura FastAPI

Arquitetura padrão para APIs desenvolvida em FastAPI.</br>

## 📑 Sumário

- [Arquitetura FastAPI](#arquitetura-fastapi)
  - [📑 Sumário](#-sumário)
  - [🗂️ Descrição dos Diretórios](#️-descrição-dos-diretórios)
    - [GitHub](#github)
    - [VSCode](#vscode)
    - [Src](#src)
    - [Src - App](#src---app)
    - [Src - App - Auto](#src---app---auto)
    - [Src - App - Backend](#src---app---backend)
    - [Src - App - Core](#src---app---core)
    - [Src - App - Database](#src---app---database)
    - [Src - App - Errors](#src---app---errors)
    - [Src - App - Interfaces](#src---app---interfaces)
    - [Src - App - Models](#src---app---models)
    - [Src - App - Repositories](#src---app---repositories)
    - [Src - App - Schemas](#src---app---schemas)
    - [Src - App - Services](#src---app---services)
    - [Src - App - Root](#src---app---root)
    - [Tests](#tests)
  - [🔑 Autenticação \& Segurança](#-autenticação--segurança)
    - [Login Token](#login-token)
    - [Novo Usuário](#novo-usuário)
    - [Novo Usuário Admin](#novo-usuário-admin)
    - [Uso do Token](#uso-do-token)
    - [Fluxo de Uso](#fluxo-de-uso)
  - [🚀 Ativação e Execução do Projeto](#-ativação-e-execução-do-projeto)
    - [Instalações Necessárias](#instalações-necessárias)
    - [Setup Inicial do Projeto](#setup-inicial-do-projeto)
    - [Execução da API e Ferramentas](#execução-da-api-e-ferramentas)
    - [Gerenciamento de Dependências](#gerenciamento-de-dependências)
    - [Qualidade de Código e Segurança](#qualidade-de-código-e-segurança)
    - [Validação Completa (Pipeline de Qualidade)](#validação-completa-pipeline-de-qualidade)
  - [🧪 Cobertura de Testes](#-cobertura-de-testes)

## 🗂️ Descrição dos Diretórios

### GitHub

Contém as definições de automação para o repositório.

### VSCode

Configurações de conveniência para o desenvolvimento local.

### Src

Raiz de todo o código fonte do projeto, isolada para garantir imports limpos e facilitar a distribuição.

### Src - App

Pacote principal que contém o núcleo do framework e a API.

### Src - App - Auto

Scripts de automação e suporte técnico.

### Src - App - Backend

Centraliza toda a lógica referente à API, como rotas, contratos de requisição (schemas) e injeções de dependências pré-definidas.

### Src - App - Core

Centraliza toda a inteligência de parâmetros e variáveis de ambiente e configurações públicas.

### Src - App - Database

Camada de infraestrutura para interações com as bases de dados.

### Src - App - Errors

Centraliza as exceções customizadas do projeto.

### Src - App - Interfaces

Armazena as interfaces de contrato (ABC) utilizados pelas classes dos módulos repositories e services.

### Src - App - Models

Representação das tabelas do banco de dados através de ORM (SQLAlchemy).

### Src - App - Repositories

Contém a lógica de negócio que lida diretamente com o banco de dados.

### Src - App - Schemas

Armazena os modelos de dados do Pydantic que definem os contratos de entrada (request) e saída (response) e outras DTOs utilizadas pelo projeto.

### Src - App - Services

Contém a lógica de negócio pura.

### Src - App - Root

### Tests

Localizado na raiz do projeto, este diretório centraliza a garantia de qualidade e a validação de todas as funcionalidades desenvolvidas.

## 🔑 Autenticação & Segurança

### Login Token

- POST /login/token → Retorna o token (apenas username e password são necessários).

```bash
curl -X 'POST' \
  'https://host:porta/login/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=string&password=<SENHA>&scope=&client_id=string&client_secret=<SECRET>'
```

- Resposta HTTP (200)

```json
{
  "access_token": "string",
  "token_type": "string"
}
```

### Novo Usuário

- POST /login/novo_usuario → Cria um novo usuário para autenticações (apenas username e password são necessários).

```bash
curl -X 'POST' \
  'https://host:8001/porta/login/novo_usuario' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'novo_usuario=string&senha_novo_usuario=string&grant_type=password&username=string&password=<SENHA>&scope=&client_id=string&client_secret=<SECRET>'
```

- Resposta HTTP (201)

```json
{
  "message": "string",
}
```

### Novo Usuário Admin

- POST /login/novo_admin → Cria um novo usuário admin para autenticações e criação de usuários.

```bash
curl -X 'POST' \
  'https://host:porta/login/novo_admin' \
  -H 'accept: application/json' \
  -d ''
```

- Resposta HTTP (201)

```json
{
  "message": "string",
}
```

***Observações***:

1. Só pode existir um usuário admin no banco de dados para cada API.</br>
2. As credenciais para o mesmo já são pré-definidas no .env e também são secretas para o código.</br>
3. Só será necessário utilizar este endpoint caso as credenciais precisem mudar.</br>
4. Apenas o usuário admin pode criar usuários novos.</br>
5. Enquanto existir um usuário admin no banco de dados, este endpoint não irá funcionar.</br>
6. O recomendado é executá-lo uma vez e com o usuário admin criar os outros usuários que utilizarão a API.

### Uso do Token

Para acessar endpoints protegidos, envie o token no header:

Código

```json
Authorization: Bearer <jwt_token>
```

### Fluxo de Uso

Login → Obtenha o token JWT.</br>
Enviar Token → Inclua Authorization: Bearer token nos headers.</br>
Consumir Endpoints → Acesse os recursos protegidos.</br>

## 🚀 Ativação e Execução do Projeto

### Instalações Necessárias

Caso ainda não possua o uv instalado na máquina:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup Inicial do Projeto

O comando uv sync substitui a preparação manual.</br>
Ele cria o ambiente virtual, instala as dependências e configura o projeto em modo editável automaticamente.

```powershell
# Sincroniza o ambiente com o lockfile (Cria .venv e instala tudo)
uv sync

# Garante que o projeto está em modo editável para permitir imports de 'src'
uv pip install -e .
```

### Execução da API e Ferramentas

Os comandos abaixo utilizam os entry points definidos no seu pyproject.toml.</br>
O uv run garante que o comando seja executado dentro do contexto do ambiente virtual.

- Subir a aplicação:
  
```powershell
uv run .\start.py
```

- Gerar Models (Banco):
  
```cmd
uv run models-script
```

run-models: Liste as tabelas desejadas em `/shared/config_models` antes de executar.</br>

### Gerenciamento de Dependências

Com o uv, não manipulamos arquivos .txt manualmente para instalar pacotes.

- Adicionar nova biblioteca:

```powershell
uv add <nome_da_biblioteca>
```

- Remover biblioteca:

```powershell
uv remove <nome_da_biblioteca>
```

- Visualizar árvore de dependências:

```powershell
uv tree
```

- Gerar/Atualizar o Lockfile:

```powershell
uv lock
```

- Atualizar o UV:

```powershell
uv self update
```

- Empacota seu código em arquivos .whl (Wheel) ou .tar.gz para distribuição oficial:

```powershell
uv build
```

### Qualidade de Código e Segurança

Centralizamos as validações no Ruff (que substitui Black, Isort, Flake8 e Pylint) e no MyPy.</br>
Para validação de segurança utilizamos o Bandit.</br>
Para idenificar código morto e bibliotecas não utilizadas, utilizamos o Vulture e o Deptry.</br>

- Validações Individuais - Linting (Erros e Boas Práticas):

```powershell
uv run ruff check .
```

- Formatação Automática:

```powershell
uv run ruff format .
```

- Análise de Tipagem Estática (Strict Mode):

```powershell
uv run mypy .
```

- Análise de Segurança (Bandit):

```powershell
uv run bandit -c pyproject.toml -r src
```

- Checagem de Dependências Inúteis (Deptry):

```powershell
uv run deptry .
```

- Checagem de Código Morto:

```powershell
uv run vulture .
```

### Validação Completa (Pipeline de Qualidade)

Para rodar todas as travas de segurança e estilo de uma só vez (recomendado antes de tentar realizar qualquer commit):

```powershell
uv run pre-commit run --all-files
```

## 🧪 Cobertura de Testes

Utilizamos o Pytest como framework principal de testes devido à sua flexibilidade e suporte a fixtures avançadas.</br>
A cobertura de código é medida para garantir que a lógica do projeto esteja sempre validada.

- Executar todos os testes:

```powershell
uv run pytest
```

Executar um teste específico:

```powershell
uv run pytest tests/unit/test_exemplo_script.py
```

Para não perder tempo rodando toda a suíte após uma correção, use a flag `--lf` (last failed):

```powershell
uv run pytest --lf
```

Para a execução no primeiro erro encontrado.

```powershell
uv run pytest -x
```

Gerar relatório de cobertura em `HTML`:

```powershell
# Abra o arquivo htmlcov/index.html no seu navegador após a execução
uv run pytest --cov=src --cov-report=html
```

---
