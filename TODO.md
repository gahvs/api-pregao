# Principais Atualizações:


### Maior Flexibilidade de Regras de Lances:
- Adicionar referencia a Regra de Lance nos Pregoes - ``DONE``
- Criar rota para definicao de Regras de Lance - ``DONE``

### Atualizacao de Catalogo:

- Adicionar Rota para definicao de Unidades, SubCategorias, Categorias, Marcas e Itens - ``DONE``
- Adicioanr campos Deleted, CreatedAt, UpdatedAt nas entidades Unidades, SubCategorias, Categorias, Marcas e Itens - ``DONE``
- Adicioanr Rotas para Alteração e Deleção nas entidades Unidades, SubCategorias, Categorias, Marcas e Itens - ``DONE``

### Maior Flexibilidade na Criação de Solicitações de Pregão:
- Remover restrição de existência de Item na criação da solicitação - ``DONE``
- Atualizar TabelaPG, model e schemas dos Itens de Solicitacao - ``DONE``
- Criar operacoes de Itens - adicionar e remover (pensar no alterar) - ``DONE``

### Maior Flexibilidade na conversão de Solicitações em Pregões:
- Recriar funcionalidade de conversão de Solicitação em Pregao - ``DONE``
- Adicionar funcionalidade de extensão de Pregão a partir de Solicitação - ``DONE``
- Testar funcionalidade de extensão de Pregão a partir de Solicitação com mais de uma solicitacao (foi testado apenas com uma)
- Testar se funcionalidade de extensão de Pregão gera erro em condicao de unidades divergentes

### Ajuste dos Status do Pregão
- Implementar novos status de Pregão
- Implementar as restrições de operação de acordo com os Status

### Melhoria da Negociação do Pregão
- Permitir alterações de Demanda durante execução do Pregão
- Adicionar aos Itens do Pregão flag de demanda atual para historico de alteração de demandas  - ``DONE``

---