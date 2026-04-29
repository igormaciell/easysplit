# Agentes de IA - EasySplit

Este diretório define agentes especializados para produzir código do MVP do EasySplit com foco em simplicidade, clareza e aderência ao `PRD.md`.

## Índice dos agentes

- [product-manager.md](./product-manager.md)  
  Define prioridade de escopo, critérios de aceite e ordem de entrega do MVP.
  Use quando for decidir o que entra ou não entra em uma sprint/tarefa.

- [backend-flask.md](./backend-flask.md)  
  Implementa rotas, blueprints, serviços e integração backend com templates.
  Use para construção de funcionalidades de aplicação Flask.

- [frontend-jinja-bootstrap.md](./frontend-jinja-bootstrap.md)  
  Implementa templates Jinja2, componentes Bootstrap e JS pontual.
  Use para páginas, navegação, formulários e feedback visual.

- [database-sqlalchemy.md](./database-sqlalchemy.md)  
  Modela entidades, relacionamentos e consultas com SQLAlchemy/SQLite.
  Use para desenho e evolução da camada de persistência.

- [auth-security.md](./auth-security.md)  
  Implementa autenticação/autorização com Flask-Login e segurança básica.
  Use para login, logout, proteção de rotas e hash de senha.

- [business-rules.md](./business-rules.md)  
  Implementa regras de divisão, saldo e sugestão de acerto.
  Use para lógica financeira centralizada e validação de consistência.

- [qa-playwright.md](./qa-playwright.md)  
  Valida fluxos reais via Playwright MCP: navegação, formulários, responsividade e consistência visual.
  Use para teste funcional ponta a ponta do MVP.

- [ui-ux.md](./ui-ux.md)  
  Garante coerência visual, legibilidade e experiência responsiva do MVP.
  Use para revisão de interface, hierarquia visual e estados vazios.

- [documentation.md](./documentation.md)  
  Mantém documentação técnica e funcional alinhada ao código real.
  Use ao finalizar entregas e atualizar `docs/`.

## Regras gerais

- Manter foco no MVP descrito no `PRD.md`.
- Não implementar funcionalidades fora de escopo.
- Não afirmar funcionalidades como prontas sem implementação real no código.
- Priorizar soluções simples e manutenção fácil.
