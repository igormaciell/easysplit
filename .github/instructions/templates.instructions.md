---
applyTo: "templates/**/*.html"
---

# Jinja2 Templates — EasySplit

## Filtros customizados obrigatórios (registrados em `app.py`)

- `{{ valor | brl }}` → formata como `R$ 1.234,56`
- `{{ data | date_br }}` → formata como `DD/MM/AAAA`

Nunca formatar moeda ou data manualmente nos templates.

## Layout base

Todos os templates estendem `templates/base.html` com `{% extends "base.html" %}`.

Blocos disponíveis: `title`, `content`.

## Padrões Bootstrap

- Classes de alerta Flash: usar `category` da mensagem como classe Bootstrap (ex: `alert-warning`, `alert-danger`, `alert-success`).
- Formulários: renderizar campos com `{{ form.campo.label }}` + `{{ form.campo(class="form-control") }}` + erros via `form.campo.errors`.
- Tabelas responsivas: envolver em `<div class="table-responsive">`.

## Segurança

- Todo formulário POST deve incluir `{{ form.hidden_tag() }}` (CSRF token do Flask-WTF).
- Nunca expor dados de outros usuários — rotas já protegem por `owner_id` ou `Participant.user_id`.

## Sem lógica de negócio

Cálculos, saldos e sugestões vêm do contexto passado pela rota. Não calcular nada nos templates.
