# Principais Atualizações:

## SOLICITACAO:
- ``EM ANDAMENTO`` Criar lógica de participantes da Solicitação, criando as entidades: ``PREGOES_SOLICITACOES_COMPRADORES`` & ``PREGOES_SOLICITACOES_FORNECEDORES``
**Tarefas**: 
    - Criar novas entidades no banco de dados seguindo estrutura do Pregão - ``DONE``
    - Criar classes *model* das entidades - ``DONE``
    - Criar classes *schemas* das entidades - ``DONE``
    - Criar classes *logic* para as entidades - ``DONE``
    - Implementar operações de adicionar e remover Compradores e Fornecedores - ``DONE``
    - Implementar operações de listagem de Compradores e Fornecedores  - ``DONE``
    - Definir os *handlers* e *endpoints* das operações  - ``DONE``
    - Implementar lógica para não permitir comprador e fornecedor na mesma solicitação (isso precisa ser validado com o time)
            
---

## PREGAO:

- ``PARA FAZER`` Refazer lógica de participantes do Pregao, hoje a API trabalha com a tabela ``PREGAO_PARTICIPANTES``, mas o Banco foi atualizado com duas novas entidades: ``PREGOES_PREGAO_COMPRADORES`` & ``PREGOES_PREGAO_FORNECEDORES``

<BR>

- ``PARA FAZER`` Desenvolver fluxo 'Criar Pregão por Solicitacao'. Receberá o ID da Solicitação aprovada, campos adicionais que apenas o Pregão possui e irá realizar a criação do PREGAO usando os itens e participantes da Solicitação.