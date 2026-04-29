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

## Padrões de implementação (quando o código for criado)

- Manter regras de negócio no backend.
- Validar dados tanto em formulário quanto no backend.
- Proteger rotas privadas com autenticação.
- Garantir que senhas sejam armazenadas com hash.
- Evitar duplicação de lógica de cálculo em rotas/templates.

## Status atual

- Estes padrões ainda não podem ser validados no código, pois a aplicação ainda não foi implementada no repositório.
