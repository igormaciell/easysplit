# 04 - Regras de negócio e qualidade

Fonte: `PRD.md`.

## Regras de negócio principais (MVP)

- Toda despesa pertence a um grupo.
- Toda despesa tem um pagador obrigatório.
- Pagador e participantes da divisão devem pertencer ao mesmo grupo.
- A divisão no MVP é igualitária.
- Saldo por participante: `saldo = total_pago - total_devido`.
- Saldo positivo indica valor a receber; negativo indica valor a pagar; zero indica quitação.
- O sistema apenas sugere acertos; pagamento acontece fora da plataforma.

## Regras de acesso

- Rotas privadas exigem autenticação.
- Usuário só pode visualizar/gerenciar dados de grupos vinculados à sua conta.

## Requisitos de qualidade (alvo do MVP)

- Interface responsiva.
- Navegação simples e objetiva.
- Consistência visual entre telas.
- Compatibilidade com navegadores modernos.
- Idioma da interface em português brasileiro.

## Status atual

- Implementado ate agora:
  - Rotas privadas de grupos, participantes e despesas usam autenticacao.
  - Acesso a grupo e recursos filhos e filtrado por `owner_id=current_user.id`.
  - Despesa sempre e criada dentro de um grupo autorizado.
  - Pagador e participantes da divisao sao validados contra o grupo atual.
  - Valor de despesa precisa ser maior que zero.
  - Divisao igualitaria e salva em `ExpenseParticipant`.
  - Remocao de participante com historico de despesa fica bloqueada.
  - Calculo de saldo usa `saldo = total_pago - total_devido`.
  - Resumo financeiro exibe total gasto, total pago, total devido, saldo e status por participante.
  - Sugestao simples de acerto conecta quem deve pagar a quem deve receber.
- Pendente:
  - Testes formais do fluxo completo.
