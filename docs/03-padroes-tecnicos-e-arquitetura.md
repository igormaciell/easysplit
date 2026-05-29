# 03 - Padrões técnicos e de arquitetura

Fonte: `PRD.md`.

## Stack planejada

- Python
- Flask
- Jinja2
- Bootstrap
- JavaScript pontual
- SQLite (MVP)
- SQLAlchemy
- Flask-Login
- Flask-WTF

## Diretrizes de arquitetura

- Arquitetura web cliente-servidor com renderização no backend (Flask + Jinja2).
- Separação por módulos/blueprints.
- Regras de cálculo centralizadas em serviço dedicado.
- Uso de templates e componentes reutilizáveis.

## Padrões de implementação

- Manter regras de negócio no backend.
- Validar dados tanto em formulário quanto no backend.
- Proteger rotas privadas com autenticação.
- Garantir que senhas sejam armazenadas com hash.
- Evitar duplicação de lógica de cálculo em rotas/templates.

## Status atual

- A aplicacao Flask usa application factory em `app.py`.
- Extensoes ficam centralizadas em `extensions.py`.
- Rotas estao separadas em blueprints (`auth` e `groups`).
- Modelos estao separados em `models/` (`User`, `Group`, `Participant`, `Expense`, `ExpenseParticipant`).
- Formularios WTForms ficam em `forms/`.
- A divisao igualitaria usada ao registrar despesas fica em `services/expense_split_service.py`.
- O calculo de saldo, status financeiro e sugestao simples de acerto fica em `services/settlement_service.py`.
