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
### [ ] Tarefa 6.2: Refinamentos

- [ ] Melhorar UI
- [ ] Validar inputs



## [ ] Sprint 7: Convites e Participacao

- [ ] Para adicionar uma pessoa em um grupo, deve ser necessario o email dela, e o sistema deve enviar um convite para ela participar do grupo. O convite deve conter um link para aceitar ou recusar a participação. Se a pessoa aceitar, ela deve ser adicionada ao grupo e receber as mesmas permissões dos outros participantes. Se a pessoa recusar, ela não deve ser adicionada ao grupo e não deve receber mais convites para aquele grupo. Logo, cada participante deve ser uma conta real no site

## [ ] Sprint 8: Nova Funcionalidade

- [ ] Adicionar funcionalidade de pagamento da divida (parcial ou total)
- [ ] Adicionar funcionalidade de exportar relatório (CSV ou PDF)
- [ ] Adicionar funcionalidade de notificações (email ou in-app)
- [ ] incluir no cadastro do usuario o numero de telefone
- [ ] Adicionar funcionalidade de autenticação via redes sociais (Google)
- [ ] Adicionar funcionalidade de chat para comunicação entre participantes

---

## [ ] Sprint 9: Testes

- [ ] Testar fluxo completo

---

## [ ] Sprint 10: Deploy (Opcional)

- [ ] Preparar produção
