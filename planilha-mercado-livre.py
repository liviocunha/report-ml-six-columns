""" GERAR NOVO RELATORIO DE PEDIDOS
    - Todos os dias o usuário exporta um relatório do Marketplace Mercado Livre, onde possui 41 colunas.
    - Porém ele tem que reduzir esse relatório somente para um relatório com 6 colunas:
    'Encomenda', 'Pedido', 'Unidades','Título do anúncio','Variação','CPF'

    - Para criar esse novo relatório, o usuário tem que se atentar as seguintes regras do negócio:
        - O Marketplace possui 2 tipos de pedidos:
            - Pedido/Encomenda com item único:
                Esse tipo de pedido é representado no relatório/planilha de pedidos somente em uma linha.
            - Pedido/Encomenda com itens múltiplos
                Esse tipo de pedido é representando por duas ou mais linhas, sendo a primeira linha que possui o número
                da encomenda e CPF do cliente
                A segunda ou mais linhas são os itens comprados que possuem o número do pedido, porém não possui o CPF
                e não possui o número da encomenda
        - O script automatiza a criação do relatório, atendendo os requisitos que o usuário utiliza"""

import pandas as pd
import argparse
from os import getcwd


class ReportML(object):

    def __init__(self, report_file_ml):

        self.report_file_ml = report_file_ml
        self.report = self._report_path(self.report_file_ml)
        self.df_report = self._read_file(self.report)
        self.filtered = self._filter_report(self.df_report)
        self.list_report_final = []

    def _report_path(self, report_file_ml):
        # Validação caso o usuário não coloque a extensão correta
        if not report_file_ml.endswith('.csv'):
            report_file_ml = report_file_ml + '.csv'

        # Buscando o diretório do Script pois a planilha deve estar no mesmo diretório
        path_report_file = str(getcwd())

        # Concatenando o caminho do arquivo com o nome do arquivo
        bar = str("/")
        path_bar_report_file = (path_report_file + bar)
        self.path_save = path_bar_report_file
        self.report = path_bar_report_file + report_file_ml
        return self.report

    def _read_file(self, report):
        # Abrindo o arquivo CSV
        self.df_report = pd.read_csv(report)
        return self.df_report

    def _filter_report(self, df_report):
        # Filtrar somente pelas colunas que importam
        self.filtered = df_report.loc[(df_report['N.º de venda'] > 0), ['N.º de venda', 'Unidades',
                                                                        'Título do anúncio',
                                                                        'Variação',
                                                                        'CPF']]
        return self.filtered

    def report_processor(self, filtered):
        # Declarando as variáveis auxiliares para processamento
        list_orders = []
        order_item_unique = []
        order_item_multiple = []
        index_multiple_items = []
        remove_line = None

        # Irá percorrer linha a linha do data frame
        for index in filtered.index:
            order_item = str(filtered['N.º de venda'][index])
            cpf = str(filtered['CPF'][index])

            # Caso a encomenda for de carrinho e não possuir CPF será atribuído na lista de multiplos itens
            # Se não é atribuído na lista de pedidos unicos
            if len(order_item) < 16:
                if cpf == " ":
                    order_item_multiple.append(index)
                else:
                    order_item_unique.append(index)
            else:
                order_item_multiple.append(index)
        # Insere na lista os indexs dos pedidos de carrinho
        for order in order_item_multiple:
            ordering = str(filtered['N.º de venda'][order])
            ordering = ordering.replace('.0', '')
            if len(ordering) == 16:
                index_multiple_items.append(order)

        # Irá percorrer novamente o data frame, porém para organizar o relatório
        for index in filtered.index:
            # Existindo na lista de pedidos únicos, popula os campos necessários para o relatório
            if index in order_item_unique:
                order_item = str(filtered['N.º de venda'][index])
                order_item = order_item.replace('.0', '')
                order = str(filtered['N.º de venda'][index])
                order = order.replace('.0', '')
                cpf = str(filtered['CPF'][index])
                units = int(filtered['Unidades'][index])
                item_title = str(filtered['Título do anúncio'][index])
                variation = str(filtered['Variação'][index])
                ordering = [order_item, order, units, item_title, variation, cpf]
                # Insere na lista de pedidos o pedido único
                list_orders.append(ordering)
            # Se não, verifica se existe dentro da lista de pedidos multiplos            
            elif index in order_item_multiple:
                # Remove o pedido de tiver o CPF vazio (pedido carrinho) e também se já estiver sido verificado
                cpf_order_item_multiple = str(filtered['CPF'][index])
                if remove_line is not None:
                    if len(index_multiple_items) > 1:
                        if cpf_order_item_multiple != " ":
                            index_multiple_items.remove(remove_line)

                # Percorre por toda a lista de pedidos multiplos 
                for order in order_item_multiple:
                    order_item = str(filtered['N.º de venda'][index])
                    order_item = order_item.replace('.0', '')
                    units = str(filtered['Unidades'][index])
                    variation = str(filtered['Variação'][index])
                    item_title = str(filtered['Título do anúncio'][index])

                    # Busca o último index do data frame
                    index_previously = index - 1
                    order_item_previously = str(filtered['N.º de venda'][index_previously])
                    order_item_previously = order_item_previously.replace('.0', '')

                    # Busca o último pedido inserido na lista de pedidos
                    last_list_order = list_orders[-1]
                    cpf_previously = str(last_list_order[5])
                    ordering_previously = str(last_list_order[0])

                    # Verifica se o pedido é de carrinho
                    if len(order_item_previously) == 16:
                        cpf = str(filtered['CPF'][index_previously])
                        order_item = str(filtered['N.º de venda'][index_previously])
                        order_item = order_item.replace('.0', '')
                    else:
                        cpf = str(filtered['CPF'][index])
                        if cpf == " ":
                            cpf = str(cpf_previously)
                            order_item = str(ordering_previously)
                            order_item = order_item.replace('.0', '')

                    # Ultima verificação para adicionar o pedido na lista de pedidos
                    for index2 in index_multiple_items:
                        order = str(filtered['N.º de venda'][index])
                        order = order.replace('.0', '')
                        ordering = [order_item, order, units, item_title, variation, cpf]
                        list_orders.append(ordering)
                        remove_line = index2
                        break
                    break

        # Cria o data frame com os itens da lista de pedidos
        report_processor = pd.DataFrame(list_orders, columns=['Ordering', 'Order', 'Unidades',
                                                              'Título do anúncio',
                                                              'Variação',
                                                              'CPF'])

        # Percorre o data frame e salva na lista final de pedidos somente os pedidos que possui itens
        for index in report_processor.index:
            ordering = str(report_processor['Ordering'][index])
            order = str(report_processor['Order'][index])
            units = str(report_processor['Unidades'][index])
            units = units.replace('.0', '')
            item_title = str(report_processor['Título do anúncio'][index])
            variation = str(report_processor['Variação'][index])
            cpf = str(report_processor['CPF'][index])
            if item_title != " ":
                ordering = [ordering, order, units, item_title, variation, cpf]
                self.list_report_final.append(ordering)
        return self.list_report_final

    def save_to_excel(self, list_report_final, name_report):
        # Salva o relatório final em planilha excel
        finale_excel = pd.DataFrame(list_report_final, columns=['Encomenda', 'Pedido', 'Unidades',
                                                                'Título do anúncio',
                                                                'Variação',
                                                                'CPF'])
        finale_excel.to_excel(self.path_save + name_report + ".xlsx", index=False)
        return finale_excel


def main():
    arguments = argparse.ArgumentParser()
    arguments.add_argument('--file', action='store', dest='report_file_ml',
                           default='', required=True,
                           help='Arquivo de extensão .csv com o relatório de vendas')
    arguments.add_argument('--relatorio-gerado', action='store', dest='relatorio_gerado',
                           default='relatorio-gerado', required=False,
                           help='Nome do relatorio gerado.')

    args = arguments.parse_args()
    report_file = args.report_file_ml
    name_report = args.relatorio_gerado

    # Instancia a classe com o nome do arquivo
    report_ml = ReportML(report_file)

    # Filtra o arquivo somente com os campos necessários
    filtered_string = report_ml.filtered

    # Processa o relatório
    report_sheet = report_ml.report_processor(filtered_string)

    # Salva a planilha final para o usuário
    report_finale_excel = report_ml.save_to_excel(report_sheet, name_report)


if __name__ == '__main__':
    main()
