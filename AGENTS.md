# AGENTS.md - Diretrizes para agentes no projeto EasySplit

## 1) Fontes de verdade

| Documento                                          | Propósito                              |
| -------------------------------------------------- | -------------------------------------- |
| [PRD.md](PRD.md)                                   | Produto, escopo e requisitos           |
| [docs/README.md](docs/README.md)                   | Índice da documentação técnica         |
| [docs/01-estado-atual.md](docs/01-estado-atual.md) | O que está implementado no código      |
| [TASKS.md](TASKS.md)                               | Roadmap de sprints e tarefas pendentes |

Se houver conflito entre decisões locais e o PRD, seguir o PRD para o MVP.

## 2) Estado atual (Sprints 0–6 concluídas)

O código-fonte está implementado. Sprints 0–6 estão entregues:

- **Infra**: application factory, blueprints, extensões centralizadas, SQLite.
- **Auth**: registro, login, logout — senha com `werkzeug.security`.
- **Grupos**: criação, listagem, dono vinculado a `User`.
- **Participantes**: adição/remoção, bloqueio quando participante tem despesas.
- **Despesas**: registro, divisão igualitária, histórico.
- **Cálculo financeiro**: saldo por participante, sugestão de acerto.
- **Dashboard**: resumo com totais, tabela de saldos e sugestões.

**Pendente**: Sprint 7 (convites por e-mail/conta real), Sprint 8 (features pós-MVP), Sprint 9 (testes), Sprint 10 (deploy).

## 3) Comandos essenciais

```bash
# Criar/ativar ambiente virtual (se ainda não existir)
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/macOS

# Instalar dependências
pip install -r requirements.txt

# Inicializar banco de dados (cria easysplit.db na raiz)
flask --app app init-db

# Rodar servidor de desenvolvimento
flask --app app run --debug
```

> `SECRET_KEY` está hardcoded como `"dev"` em `app.py`. Para produção, mover para variável de ambiente.

## 4) Objetivo do agente

Implementar o MVP do EasySplit com foco em:

- Fluxo principal completo: cadastro, login, grupos, participantes, despesas, resumo e acerto.
- Simplicidade de implementação e clareza de UX.
- Regras de negócio no backend.

## 5) Restrições obrigatórias

- Não documentar ou afirmar funcionalidades como prontas sem código implementado.
- Não implementar itens fora do MVP nesta fase.
- Não adicionar integração de pagamento real (incluindo Pix), banco externo, app nativo, múltiplas moedas, notificações externas, convite por link ou PDF.
- Toda interface de usuário final deve estar em português brasileiro.

## 6) Stack alvo do MVP

- Python + Flask
- Jinja2 + Bootstrap + JavaScript pontual
- SQLite
- SQLAlchemy
- Flask-Login
- Flask-WTF

## 7) Padrões de arquitetura e código

- Usar application factory (`create_app()` em `app.py`).
- Organizar por módulos/blueprints (`auth`, `groups`, futuros: `expenses`, `invitations`).
- Centralizar extensões em `extensions.py` (`db`, `login_manager`).
- Centralizar cálculos financeiros em `services/settlement_service.py`; divisão igualitária em `services/expense_split_service.py`.
- Formulários WTForms em `forms/`; nunca validar apenas no template.
- Evitar lógica de negócio em templates.
- Validar entrada em formulário **e** backend.
- Proteger rotas privadas com `@login_required`.
- Armazenar senha somente com hash (`werkzeug.security`).
- Usar os filtros Jinja2 customizados `| brl` (moeda BRL) e `| date_br` (data DD/MM/AAAA) registrados em `app.py`.

### Mapa de arquivos-chave

| Arquivo                             | Responsabilidade                                                                                      |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `app.py`                            | Application factory, filtros Jinja2, CLI `init-db`                                                    |
| `extensions.py`                     | Instâncias de `db` e `login_manager`                                                                  |
| `models/`                           | SQLAlchemy models: `User`, `Group`, `Participant`, `Expense`, `ExpenseParticipant`, `GroupInvitation` |
| `routes/auth.py`                    | Registro, login, logout                                                                               |
| `routes/groups.py`                  | Grupos, participantes, despesas, dashboard                                                            |
| `services/settlement_service.py`    | `calculate_group_summary()` → saldos e sugestões de acerto                                            |
| `services/expense_split_service.py` | `split_amount_equally()` → divisão igualitária com centavos corretos                                  |
| `forms/`                            | WTForms para cada entidade (auth, group, participant, expense, invitation)                            |
| `templates/base.html`               | Layout base Bootstrap                                                                                 |
| `templates/groups/detail.html`      | Tela principal: participantes, despesas, dashboard                                                    |

## 8) Regras de negócio que não podem ser quebradas

- Despesa sempre pertence a um grupo.
- Despesa sempre possui pagador.
- Pagador e participantes da divisão pertencem ao mesmo grupo.
- Divisão do MVP é igualitária.
- Fórmula de saldo: `saldo = total_pago - total_devido`.
- Sistema sugere acertos, mas não executa pagamento.
- Usuário só acessa dados de grupos vinculados à própria conta.

## 9) Ordem de execução recomendada

Seguir o roadmap do PRD:

1. Base do projeto Flask + configuração + banco.
2. Autenticação (cadastro/login/logout).
3. Grupos e participantes.
4. Despesas e histórico.
5. Serviço de cálculo, resumo e sugestão de acerto.
6. Polimento de UX, responsividade, validações e segurança.
7. QA final e documentação.

## 10) Critério de conclusão do MVP

Considerar MVP concluído apenas quando:

- Fluxo principal estiver funcional ponta a ponta.
- Rotas privadas estiverem protegidas.
- Senhas estiverem com hash.
- Resumo financeiro e acertos refletirem corretamente os dados de despesas.
- Interface principal estiver responsiva.
- Escopo fora do MVP permanecer fora da entrega.

## 11) Atualização de documentação

A cada entrega relevante:

- Atualizar arquivos em `docs/` apenas com o que estiver implementado de fato.
- Evitar backlog técnico implícito: registrar gaps de forma explícita.

---

## 12) Critérios de Avaliação Técnica (Auditoria)

Os 7 critérios abaixo serão avaliados na entrega. Verificar antes de submeter:

| #   | Critério                                  | Como está coberto no projeto                                                            |
| --- | ----------------------------------------- | --------------------------------------------------------------------------------------- |
| 1   | Application Factory / Arquitetura modular | `create_app()` em `app.py`, extensões em `extensions.py`                                |
| 2   | Blueprints / Módulos / Rotas              | `routes/auth.py` e `routes/groups.py` registrados em `create_app()`                     |
| 3   | Formulários com validação server-side     | Flask-WTF + WTForms em `forms/`, validação dupla (form + backend)                       |
| 4   | Templates / Frontend responsivo           | Jinja2 + Bootstrap em `templates/`, filtros `\| brl` e `\| date_br`                     |
| 5   | Testes automatizados                      | **Pendente — Sprint 9.** Ver instruções em `.github/instructions/tests.instructions.md` |
| 6   | ORM / Persistência                        | SQLAlchemy models em `models/`, SQLite via `easysplit.db`                               |
| 7   | Qualidade / .env / logging / erros        | Ver `.github/instructions/backend.instructions.md` — `SECRET_KEY` deve ir para `.env`   |

## 13) Checklist de Entrega

### Arquivo ZIP

- Compactar todos os arquivos **exceto** `venv/`, `__pycache__/`, `.git/` e `easysplit.db`.
- Nome: `GrupoX_EasySplit.zip`

### Documento PDF (obrigatório)

O PDF deve conter:

1. Título do projeto e nomes dos integrantes
2. Descrição geral do produto e funcionalidades
3. Diagrama ER do banco de dados (tabelas: `users`, `groups`, `participants`, `expenses`, `expense_participants`, `group_invitations`)
4. Detalhamento técnico das principais partes do código (trechos relevantes)
5. Explicação da arquitetura adotada (Application Factory, Blueprints, Services)
6. Tecnologias utilizadas e justificativa (Flask, SQLAlchemy, WTForms, Bootstrap)
7. Como rodar o projeto (passo a passo — basear nos comandos da seção 3)
8. Principais desafios encontrados e como foram resolvidos

> Projetos sem PDF ou com código incompleto têm os critérios técnicos avaliados apenas pela apresentação.
