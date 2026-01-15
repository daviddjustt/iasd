# 🏛️ Módulo de Ministérios

## Visão Geral
Este módulo gerencia a estrutura organizacional da igreja. Ele define quem são os líderes, quais membros pertencem a cada grupo e serve como base para a responsabilidade dos eventos.

## Modelos de Dados

### Ministério
| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | UUID | Identificador único (Gerado automaticamente). |
| `nome` | String | Nome do ministério (ex: Louvor, Jovens). |
| `lider` | FK (Membro) | UUID do membro responsável pelo ministério. |
| `membros` | M2M (Membro) | Lista de membros associados ao ministério. |

## Endpoints Principais (API)

### `GET /api/ministerios/`
Lista todos os ministérios cadastrados.

### `GET /api/ministerios/{id}/resumo-atividades/`
Endpoint customizado para Dashboards.
- **Retorno:** Total de eventos, contagem de membros e os próximos 3 agendamentos cronológicos.

## Regras de Negócio
1. **Liderança:** Um ministério pode ficar sem líder temporariamente (`null`), mas não pode ser deletado se houver eventos vinculados a ele (proteção de integridade).
2. **Membros:** Um membro pode participar de múltiplos ministérios simultaneamente.