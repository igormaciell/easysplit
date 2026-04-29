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

- As regras acima representam critérios de implementação e validação futura.
- Ainda não há código para verificação automática desses critérios no repositório.
