# 01 - Estado atual do projeto

## Implementado no codigo

- Estrutura Flask com application factory em `app.py`.
- Extensoes centralizadas em `extensions.py` (`SQLAlchemy`, `Flask-Login`).
- Autenticacao completa do MVP (Sprint 1):
  - Registro, login e logout.
  - Senha armazenada com hash (`werkzeug.security`).
  - Rotas privadas protegidas com `@login_required`.
- Sprint 2 entregue (Grupos):
  - Model `Group` com vinculo de dono (`owner_id -> users.id`).
  - Relacao `User.groups`.
  - Criacao de grupo por formulario.
  - Listagem de grupos do usuario autenticado.
- Sprint 3 entregue conforme `TASKS.md` (Participantes):
  - Model `Participant` vinculado obrigatoriamente a `Group`.
  - Pagina de detalhe do grupo com listagem de participantes.
  - Adicao de participante por formulario.
  - Bloqueio de nomes vazios e duplicidades evidentes no mesmo grupo.
  - Remocao de participante sem historico financeiro.
  - Bloqueio de remocao quando o participante ja aparece como pagador ou na divisao de despesa.
- Sprint 4 entregue conforme `TASKS.md` (Despesas):
  - Models `Expense` e `ExpenseParticipant`.
  - Formulario de despesa dentro da pagina do grupo.
  - Validacao de titulo, valor maior que zero, data, pagador e participantes da divisao.
  - Validacao backend para garantir pagador e participantes pertencentes ao grupo.
  - Salvamento da divisao igualitaria em `ExpenseParticipant`.
  - Historico de despesas com data, titulo, valor, pagador e participantes da divisao.
- Sprint 5 entregue conforme `TASKS.md` (Calculo CORE):
  - Servico `settlement_service.py` para calculo financeiro.
  - Calculo de `total_pago`, `total_devido` e `saldo` por participante.
  - Classificacao de saldo como `A receber`, `A pagar` ou `Quitado`.
  - Sugestao simples de acerto entre devedores e recebedores.
- Sprint 6 entregue conforme `TASKS.md` (Dashboard):
  - Cards de total gasto, quantidade de participantes, quantidade de despesas e maior despesa.
  - Tabela de resumo financeiro por participante.
  - Exibicao de sugestoes de acerto ou estado vazio quando nao houver pendencias.
- Comando `flask --app app init-db` para criar tabelas do SQLite local.

## Limites atuais

- Nao ha edicao ou exclusao de despesas.
- Ainda nao ha testes formais versionados do fluxo completo.
- Fluxo principal ainda depende das sprints 7 e 8 de `TASKS.md`.
