# AGENTS.md - Diretrizes para agentes no projeto EasySplit

## 1) Fonte de verdade

- Produto e escopo: `PRD.md`
- Índice de documentação: `docs/README.md`
- Estado atual: o repositório ainda não contém código-fonte da aplicação, apenas planejamento (`PRD.md`) e ambiente virtual (`venv/`).

Se houver conflito entre decisões locais e o PRD, seguir o PRD para o MVP.

## 2) Objetivo do agente

Implementar o MVP do EasySplit com foco em:

- Fluxo principal completo: cadastro, login, grupos, participantes, despesas, resumo e acerto.
- Simplicidade de implementação e clareza de UX.
- Regras de negócio no backend.

## 3) Restrições obrigatórias

- Não documentar ou afirmar funcionalidades como prontas sem código implementado.
- Não implementar itens fora do MVP nesta fase.
- Não adicionar integração de pagamento real (incluindo Pix), banco externo, app nativo, múltiplas moedas, notificações externas, convite por link ou PDF.
- Toda interface de usuário final deve estar em português brasileiro.

## 4) Stack alvo do MVP

- Python + Flask
- Jinja2 + Bootstrap + JavaScript pontual
- SQLite
- SQLAlchemy
- Flask-Login
- Flask-WTF

## 5) Padrões de arquitetura e código

- Usar application factory.
- Organizar por módulos/blueprints (`auth`, `groups`, `expenses`, etc.).
- Centralizar extensões em `extensions.py`.
- Centralizar regras de cálculo de saldos/acertos em serviço dedicado (ex.: `settlement_service.py`).
- Evitar lógica de negócio em templates.
- Validar entrada em formulário e backend.
- Proteger rotas privadas com autenticação.
- Armazenar senha somente com hash.

## 6) Regras de negócio que não podem ser quebradas

- Despesa sempre pertence a um grupo.
- Despesa sempre possui pagador.
- Pagador e participantes da divisão pertencem ao mesmo grupo.
- Divisão do MVP é igualitária.
- Fórmula de saldo: `saldo = total_pago - total_devido`.
- Sistema sugere acertos, mas não executa pagamento.
- Usuário só acessa dados de grupos vinculados à própria conta.

## 7) Ordem de execução recomendada

Seguir o roadmap do PRD:

1. Base do projeto Flask + configuração + banco.
2. Autenticação (cadastro/login/logout).
3. Grupos e participantes.
4. Despesas e histórico.
5. Serviço de cálculo, resumo e sugestão de acerto.
6. Polimento de UX, responsividade, validações e segurança.
7. QA final e documentação.

## 8) Critério de conclusão do MVP

Considerar MVP concluído apenas quando:

- Fluxo principal estiver funcional ponta a ponta.
- Rotas privadas estiverem protegidas.
- Senhas estiverem com hash.
- Resumo financeiro e acertos refletirem corretamente os dados de despesas.
- Interface principal estiver responsiva.
- Escopo fora do MVP permanecer fora da entrega.

## 9) Atualização de documentação

A cada entrega relevante:

- Atualizar arquivos em `docs/` apenas com o que estiver implementado de fato.
- Evitar backlog técnico implícito: registrar gaps de forma explícita.
