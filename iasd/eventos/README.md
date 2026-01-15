# 📅 Módulo de Eventos e Agendamentos

## Visão Geral
Responsável pela gestão de agenda da igreja. Permite que um único evento (ex: "Semana de Oração") possua múltiplos horários e datas independentes.

## Modelos de Dados

### Evento
Estrutura principal que define o "O Quê" e "Onde".
- `ministerio_responsavel`: FK para o Ministério.
- `endereco`: Local de realização.
- `tematica`: Nome ou descrição do evento.

### Agendamento
Define o "Quando". Relacionado ao Evento via ForeignKey (1:N).
- `data`: Data do evento.
- `horario_inicio` / `horario_final`: Intervalo de tempo.

## Lógica de Validação de Conflitos (POST /api/eventos/)

Ao criar um novo evento com seus respectivos horários, o sistema aplica as seguintes regras:

| Cenário | Resultado | Resposta HTTP |
| :--- | :--- | :--- |
| Sobreposição no **mesmo** ministério | **Bloqueio total** | `400 Bad Request` |
| Sobreposição em ministérios **diferentes** | **Permitido com Aviso** | `201 Created` + Header `X-Warning` |
| Sem sobreposição | **Sucesso** | `201 Created` |



## Endpoints para o Frontend

### `GET /api/eventos/calendario/`
Retorna os dados agrupados por data. Ideal para bibliotecas de calendário (FullCalendar, etc).
```json
{
  "2026-01-15": [
    { "tematica": "Culto Jovem", "horario": "19:00 - 21:00" }
  ]
}