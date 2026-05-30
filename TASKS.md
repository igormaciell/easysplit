# TASKS.md - EasySplit

## [x] Sprint 0: Setup Inicial

### [x] Tarefa 0.1: Configuração do Ambiente

- [x] Criar diretório do projeto
- [x] Criar ambiente virtual
- [x] Instalar Flask, SQLAlchemy, Flask-Login, Flask-WTF
- [x] Criar requirements.txt
- [x] Criar .gitignore

### [x] Tarefa 0.2: Estrutura Base

- [x] Criar app.py
- [x] Criar estrutura:
  - models/
  - routes/
  - templates/
  - static/

---

## [x] Sprint 1: Autenticação

### [x] Tarefa 1.1: Model User

- [x] Criar model User
- [x] Implementar senha com hash

### [x] Tarefa 1.2: Login/Registro

- [x] Criar rota /login
- [x] Criar rota /register
- [x] Criar templates

---

## [x] Sprint 2: Grupos

### [x] Tarefa 2.1: Model Grupo

- [x] Criar model Grupo

### [x] Tarefa 2.2: CRUD Grupo

- [x] Criar grupo
- [x] Listar grupos

---

## [x] Sprint 3: Participantes

### [x] Tarefa 3.1: Model Participante

- [x] Criar model

### [x] Tarefa 3.2: CRUD Participantes

- [x] Adicionar participante
- [x] Remover participante

---

## [x] Sprint 4: Despesas

### [x] Tarefa 4.1: Model Despesa

- [x] Criar model

### [x] Tarefa 4.2: Registro de Despesas

- [x] Criar formulário
- [x] Salvar despesa

---

## [x] Sprint 5: Cálculo (CORE)

### [x] Tarefa 5.1: Lógica de divisão

- [x] Calcular divisão igualitária

### [x] Tarefa 5.2: Saldo

- [x] Calcular quem deve/paga

---

## [x] Sprint 6: Dashboard

### [x] Tarefa 6.1: Tela resumo

- [x] Exibir saldo por participante
- [x] Exibir total gasto

---

### [x] Tarefa 6.2: Qualidade e Boas Práticas

#### 6.2.1 Variáveis de Ambiente

- [x] Instalar `python-dotenv` e adicionar ao `requirements.txt`
- [x] Criar arquivo `.env` na raiz com `SECRET_KEY=<valor-secreto>`
- [x] Criar arquivo `.env.example` (sem valores reais) para referência
- [x] Atualizar `app.py` para ler `SECRET_KEY` de `os.environ` com fallback `"dev"`
- [x] Confirmar que `.env` está no `.gitignore` (já está)

#### 6.2.2 Tratamento de Erros

- [x] Criar pasta `templates/errors/`
- [x] Criar `templates/errors/404.html` estendendo `base.html`
- [x] Criar `templates/errors/500.html` estendendo `base.html`
- [x] Registrar handlers `@app.errorhandler(404)` e `@app.errorhandler(500)` em `create_app()`

#### 6.2.3 Logging

- [x] Substituir qualquer `print()` de debug por `app.logger.info()` / `app.logger.error()`
- [x] Configurar nível de log em desenvolvimento: `app.logger.setLevel(logging.DEBUG)` quando `DEBUG=True`

#### 6.2.4 Refinamentos de UI

- [x] Validar que todos os formulários exibem mensagens de erro inline (Bootstrap `is-invalid`)
- [x] Verificar responsividade em mobile da tela de detalhe do grupo
- [x] Garantir estado vazio amigável quando grupo não tiver participantes nem despesas

---

## [x] Sprint 7: Convites e Participação

### [x] Tarefa 7.1: Model e Formulário

- [x] Criar model `GroupInvitation` com campos `group_id`, `invited_user_id`, `invited_by_user_id`, `status`, `created_at`, `responded_at`
- [x] Criar `forms/invitation.py` com validação de e-mail

### [x] Tarefa 7.2: Rotas de Convite

- [x] `POST /<group_id>/invitations` — enviar convite (apenas dono do grupo)
- [x] `POST /invitations/<invite_id>/accept` — aceitar convite
- [x] `POST /invitations/<invite_id>/decline` — recusar convite
- [x] Validações: e-mail deve ser de conta existente, sem convite duplicado, convite recusado não pode ser reenviado

### [x] Tarefa 7.3: Templates

- [x] Formulário de convite na página de detalhe do grupo (visível apenas ao dono)
- [x] Lista de convites pendentes/recusados na página de detalhe (visível apenas ao dono)
- [x] Lista de convites pendentes para o usuário na página de listagem de grupos (`groups/index.html`)
- [x] Botões "Aceitar" e "Recusar" com formulários CSRF-protegidos

### [x] Tarefa 7.4: Lógica de Aceitação

- [x] Ao aceitar, criar `Participant` vinculado ao `User` (ou vincular ao participante anônimo de mesmo nome, se existir)
- [x] Garantir que usuário convidado acessa o grupo após aceitar

---

## [ ] Sprint 8: Funcionalidades Pós-MVP (fora do escopo atual)

> Não implementar nesta fase. Registrado para planejamento futuro.

- [ ] Pagamento parcial ou total da dívida
- [ ] Exportação de relatório (CSV ou PDF)
- [ ] Notificações por e-mail ou in-app
- [ ] Telefone no cadastro de usuário
- [ ] Autenticação via Google (OAuth)
- [ ] Chat entre participantes do grupo

---

## [x] Sprint 9: Testes Automatizados

> Critério de avaliação obrigatório. Ver instruções completas em `.github/instructions/tests.instructions.md`.

### [x] Tarefa 9.1: Infraestrutura de Testes

- [x] Instalar `pytest` e `pytest-flask`, adicionar ao `requirements.txt`
- [x] Criar pasta `tests/`
- [x] Criar `tests/__init__.py`
- [x] Criar `tests/conftest.py` com fixtures `app`, `db` (SQLite em memória) e `client`
  - `WTF_CSRF_ENABLED=False` obrigatório na config de teste
  - `SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"`

### [x] Tarefa 9.2: Testes de Autenticação (`tests/test_auth.py`)

- [x] `test_register_success` — POST `/auth/register` cria usuário e redireciona
- [x] `test_register_duplicate_email` — segundo cadastro com mesmo e-mail retorna erro
- [x] `test_login_success` — login com credenciais corretas redireciona para grupos
- [x] `test_login_wrong_password` — login com senha errada retorna 200 com erro
- [x] `test_logout` — logout redireciona para login
- [x] `test_protected_route_redirects_unauthenticated` — GET `/groups/` sem login redireciona para `/auth/login`

### [x] Tarefa 9.3: Testes de Grupos e Participantes (`tests/test_groups.py`)

- [x] `test_create_group` — POST cria grupo e adiciona dono como participante automaticamente
- [x] `test_list_groups_only_own` — usuário B não vê grupos do usuário A
- [x] `test_add_participant` — participante adicionado via DB aparece na página do grupo
- [x] `test_remove_participant_without_expenses` — remoção bem-sucedida
- [x] `test_remove_participant_with_expenses_blocked` — remoção bloqueada retorna aviso

### [x] Tarefa 9.4: Testes de Despesas (`tests/test_expenses.py`)

- [x] `test_add_expense_success` — despesa registrada com divisão igualitária
- [x] `test_add_expense_zero_value_rejected` — valor ≤ 0 retorna erro de validação
- [x] `test_expense_history_visible` — despesa aparece no histórico da página de detalhe

### [x] Tarefa 9.5: Testes de Serviços (`tests/test_services.py`)

- [x] `test_split_equally_exact` — R$ 30,00 ÷ 3 = R$ 10,00 cada
- [x] `test_split_equally_with_remainder` — R$ 10,00 ÷ 3 = R$ 3,34 + R$ 3,33 + R$ 3,33
- [x] `test_calculate_summary_balance` — saldo correto: `total_pago - total_devido`
- [x] `test_calculate_summary_settlement_suggestion` — sugestão gerada quando há devedores e credores

### [x] Tarefa 9.6: Testes de Convites (`tests/test_invitations.py`)

- [x] `test_invite_by_email_success` — convite criado com status `pending`
- [x] `test_invite_nonexistent_email` — e-mail sem conta retorna erro
- [x] `test_accept_invitation` — status muda para `accepted` e participante é criado
- [x] `test_decline_invitation` — status muda para `declined`

---

## [ ] Sprint 10: Entrega

### [ ] Tarefa 10.1: Qualidade Final

- [ ] Executar `pytest tests/ -v` e garantir que todos os testes passam
- [ ] Revisar `requirements.txt` — garantir que `pytest`, `pytest-flask` e `python-dotenv` estão incluídos
- [ ] Confirmar que `SECRET_KEY` é lida do `.env` e não está hardcoded para produção
- [ ] Verificar que `.env` e `easysplit.db` estão no `.gitignore`
- [ ] Testar fluxo completo manual: registro → login → grupo → convite → despesa → dashboard → acerto

### [ ] Tarefa 10.2: Empacotamento (ZIP)

- [ ] Compactar todos os arquivos **exceto**:
  - `venv/` — ambiente virtual
  - `__pycache__/` e `*.pyc` / `*.pyo` — bytecode Python
  - `.git/` — histórico Git
  - `*.db` / `*.sqlite3` — banco de dados local (`easysplit.db`)
  - `.env` — variáveis de ambiente com segredos
  - `.pytest_cache/` e `.mypy_cache/` — cache de ferramentas
  - `.vscode/` e `.idea/` — configurações de IDE
  - `.copilot/`, `.cursor/`, `.windsurf/`, `.cline/`, `.aider*` — caches e configs locais de ferramentas de IA
  - `.coverage` e `htmlcov/` — relatórios de cobertura de testes
  - `dist/`, `build/`, `*.egg-info/` — artefatos de build
- [ ] Nomear o arquivo: `GrupoX_EasySplit.zip`
- [ ] Validar que o ZIP contém: `app.py`, `requirements.txt`, `models/`, `routes/`, `services/`, `forms/`, `templates/`, `static/`, `tests/`, `.env.example`

### [ ] Tarefa 10.3: Documento PDF (obrigatório)

- [ ] **Título do projeto** e nomes dos integrantes
- [ ] **Descrição geral** do produto e funcionalidades
- [ ] **Diagrama ER** do banco (tabelas: `users`, `groups`, `participants`, `expenses`, `expense_participants`, `group_invitations`)
- [ ] **Detalhamento técnico** das principais partes do código (trechos relevantes de `app.py`, `settlement_service.py`, `routes/groups.py`)
- [ ] **Arquitetura adotada** (Application Factory, Blueprints `auth` + `groups`, Services, WTForms)
- [ ] **Tecnologias utilizadas** e justificativa (Flask, SQLAlchemy, WTForms, Bootstrap, Flask-Login)
- [ ] **Como rodar o projeto** (passo a passo baseado nos comandos do `AGENTS.md` seção 3)
- [ ] **Principais desafios** encontrados e como foram resolvidos
