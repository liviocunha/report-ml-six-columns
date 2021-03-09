# Script para automatizar processo de gerar relatório enxuto

### User Story
- Todos os dias o usuário exporta um relatório do Marketplace Mercado Livre, onde possui 41 colunas e dezenas de linhas.
    - Porém o usuário tem que reduzir esse relatório somente para um relatório com 6 colunas:
   
    | Encomenda| Pedido| Unidades | Título do anúncio | Variação | CPF
    |-----|-----|----|----|-----|-----|
    
    - Para criar esse novo relatório, o usuário tem que se atentar as seguintes regras do negócio:
        - O Marketplace possui 2 tipos de pedidos:
            - Pedido/Encomenda com item único: 
            > Esse tipo de pedido é representado no relatório/planilha de pedidos somente em uma linha.
            - Pedido/Encomenda com itens múltiplos:
            > Esse tipo de pedido é representando por duas ou mais linhas, sendo a primeira linha que possui o número da encomenda e CPF do cliente.
            > A segunda ou mais linhas são os itens comprados que possuem o número do pedido, porém não possui o CPF e não possui o número da encomenda
        - O novo relatório deve conter todos os itens vendidos separados por linhas e com as informações das 6 colunas informadas acima.

## Tecnologias Utilizadas
Foi utilizado a linguagem Python 3.8.5. Seguintes bibliotecas foram utilizadas:
- **pandas** para processar e manipular as informações da planilha
- **argparse** para tratar argumentos passados pelo terminal

## Executando o Script
O script é executado na linha de comando e possui dois parâmetros:
- [--file]: argumento obrigatório onde deve-se passar o nome do relatório de vendas
    > **Obs.:** O relatório de vendas deve estar no mesmo diretório do Script
- [--relatorio-gerado]: argumento opcional para informar o nome do novo relatório gerado.
    > Caso não seja passado o argumento o relatório é gerado com o nome padrão *relatorio-gerado*

Exemplo de uso:      
        
      python3 planilha-mercado-livre.py --file relatorio_vendas_exemplo --relatorio-gerado novo-relatorio
