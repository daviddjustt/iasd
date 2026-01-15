# 🛠️ Guia de Gerenciamento de Dependências (Django + Docker + Celery)

Este guia descreve o fluxo correto para instalar, configurar e verificar novas bibliotecas no projeto **IASD**, garantindo que tanto o container Django quanto os containers do Celery (Worker e Beat) reconheçam as mudanças.

---

## 1. Adicionar a Dependência
O projeto utiliza o padrão `pyproject.toml` (moderno). Nunca instale via `pip install` manualmente dentro de um container rodando.

1. Abra o arquivo `pyproject.toml`.
2. Vá até a seção `dependencies`.
3. Adicione a biblioteca seguindo o padrão: `"nome-da-lib==versao"`.

**Exemplo:**
```toml
dependencies = [
    "django-filter==25.1",
    "djangorestframework==3.16.1",
]

```

---

## 2. Registrar no Django

Se a biblioteca for um App do Django (como `django-filter` ou `rest_framework`), adicione-a ao arquivo de configuração:

**Arquivo:** `config/settings/base.py`

```python
THIRD_PARTY_APPS = [
    "django_filters",  # Use sempre underline (_) aqui
    "rest_framework",
]

```

---

## 3. Reconstruir o Ambiente (Build)

O Docker precisa "assar" uma nova imagem com as novas instruções. O uso do `--no-cache` é recomendado para evitar que o Docker ignore mudanças sutis nos arquivos de texto.

```bash
# 1. Derrube os containers atuais
docker compose -f docker-compose.local.yml down

# 2. Reconstrua a imagem do Django (base para Celery)
docker compose -f docker-compose.local.yml build --no-cache django

```

---

## 4. Validar a Instalação

Sempre valide se a biblioteca está presente antes de subir todo o sistema.

### Nível 1: Verificação de Arquivo (Pip)

```bash
docker compose -f docker-compose.local.yml run --rm django pip list | grep django-filter

```

### Nível 2: Verificação de Importação (Python)

```bash
docker compose -f docker-compose.local.yml run --rm django python -c "import django_filters; print('Sucesso!')"

```

---

## 5. Sincronizar Celery e Serviços

Como os serviços `celeryworker`, `celerybeat` e `flower` compartilham a imagem do `django`, eles precisam ser recriados para "enxergar" o novo pacote instalado.

Execute:

```bash
docker compose -f docker-compose.local.yml up -d --force-recreate

```

---

## 🚀 Troubleshooting (Resolução de Problemas)

| Problema | Causa Provável | Solução |
| --- | --- | --- |
| `ModuleNotFoundError` no Celery | Containers antigos presos na memória. | Use `--force-recreate` no `up`. |
| `pip list` não mostra a lib | `pyproject.toml` não foi salvo ou build usou cache. | Verifique o arquivo e use `--no-cache`. |
| `bash: !: event not found` | Caractere especial `!` no terminal Linux. | Evite usar `!` em comandos de print no terminal. |
| Erro de import no Django | Nome no `INSTALLED_APPS` está errado. | Verifique se é com hífen `-` ou underline `_`. |

```