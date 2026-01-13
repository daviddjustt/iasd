# IASD Controle de visitas

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)

![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=flat&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%232496ED.svg?style=flat&logo=docker&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=flat&logo=ubuntu&logoColor=white)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


Sistema para gerenciamento e controle de visitas da IASD.

**Licença:** MIT

---

## 🚀 Início Rápido

Siga os passos abaixo para configurar seu ambiente de desenvolvimento local.

### 1. Pré-requisitos
Certifique-se de ter instalado:
* **Docker** e **Docker Compose**
* **Python 3.12+** (opcional, para ambiente local da IDE)

### 2. Ambiente Virtual (Para desenvolvimento na IDE)
Se você deseja que o VS Code ou PyCharm reconheçam os imports do projeto:

```bash
    # Criar o ambiente virtual
    python3 -m venv .venv

    # Ativar
    source .venv/bin/activate

    # Instalar dependências locais
    pip install -r requirements.txt
```

### 3. Rodando com Docker (Ambiente Local)

O Docker gerencia o banco de dados Postgres, Redis e a aplicação Django automaticamente.

**Construir as imagens (Build):**

```bash
    docker compose -f docker-compose.local.yml build

```

**Subir os containers:**

```bash
    docker compose -f docker-compose.local.yml up

```

**Parar os containers:**

```bash
    docker compose -f docker-compose.local.yml down

```

> **Dica:** Se houver erro de permissão no Docker (Linux), lembre-se de rodar com `sudo` ou adicionar seu usuário ao grupo `docker`.

### 4. Comandos de Administração

Com os containers rodando, abra um novo terminal para executar estes comandos:

**Criar um superusuário (Acesso ao /admin):**

```bash
    docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser

```

**Rodar Migrations:**

```bash
    docker compose -f docker-compose.local.yml run --rm django python manage.py makemigrationss
    docker compose -f docker-compose.local.yml run --rm django python manage.py migrate

```

**Rodar Testes com Pytest:**

```bash
    docker compose -f docker-compose.local.yml run --rm django pytest

```

---

## 🛠️ Manutenção

Para limpar volumes e imagens antigas que possam estar causando conflitos:

```bash
    docker compose -f docker-compose.local.yml down --volumes --remove-orphans

```