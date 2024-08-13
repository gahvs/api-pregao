# Principais Atualizações:

## SOLICITACAO:
- Criar lógica de participantes da Solicitação, criando as entidades: ``PREGOES_SOLICITACOES_COMPRADORES`` & ``PREGOES_SOLICITACOES_FORNECEDORES``


## PREGAO:

- Refazer lógica de participantes do Pregao, hoje a API trabalha com a tabela ``PREGAO_PARTICIPANTES``, mas o Banco foi atualizado com duas novas entidades: ``PREGOES_PREGAO_COMPRADORES`` & ``PREGOES_PREGAO_FORNECEDORES``

- Desenvolver fluxo 'Criar Pregão por Solicitacao'. Receberá o ID da Solicitação aprovada, campos adicionais que apenas o Pregão possui e irá realizar a criação do PREGAO usando os itens e participantes da Solicitação.