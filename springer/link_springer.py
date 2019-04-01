from wget import download
from requests import get
from bs4 import BeautifulSoup
from pandas import read_csv, DataFrame
from numpy import array

""" Algoritmo para realizar download de arquivos do site Springer

1. Recebe uma lista no formato .csv (extraída do site Springer)
2. Processa essa lista buscando cada resumo.
3. Avalia se o resumo é compatível com a String de busca.
3.1 Se sim, baixa e arquiva processamento
3.2 Se não, apenas arquiva o processamento 
4. Salva uma lista de processamento na pasta
 
"""


def analisar_string(resumo):
    """Analisar se um resumo contém as palavras-chave da String de busca.

    Parâmetro:
        resumo: Resumo coletado de um artigo.

    Retorno:
        bool: Retorna o valor. Verdadeiro para conter palavras-chave, falso caso contrário
     """

    resumo = resumo.lower()  # Transforme o texto em caixa baixa.

    # Determina as palavras da String de busca
    palavra_1 = resumo.count('gateway')
    palavra_2 = resumo.count('middleware')
    palavra_3 = resumo.count('internet of things')
    palavra_4 = resumo.count('iot')
    palavra_5 = resumo.count('security')

    # Construa sua sentença de busca String usando os operadorees lógicos.
    if (palavra_1 or palavra_2) and (palavra_3 or palavra_4) and palavra_5:
        return True
    else:
        return False


def coletar_resumo(url):
    """Coletar resumos com base em uma url;

       Parâmetro:
           url: Link da página do artigo Springer

       Retorno:
           resumo: Retorna o resumo do artigo, caso haja.

    """
    html_completo = get(url)
    soup_completo = BeautifulSoup(html_completo.content, 'html.parser')
    sections = soup_completo.findAll("section")
    resumo = 'No abstract found!'
    for section in sections:
        try:
            if section['class'] == ['Abstract']:
                resumo = section.findChild('p').text
                break
        except KeyError:
            """ Nenhuma tag Secion['Class'] encontrada.
            
            Este erro é obtido quando não há nenhum seção com classe
            Porém, este erro não relata artigos sem abstract. Pode ocorrer, por
            exemplo, de haver uma section com class sem abstract. 
            
            Portanto, são dois erros diferentes, ter abstract ou ter class em section.
            """
            print('No tag class section found in this article!')

    return resumo


def baixar_artigo(title, year, doi):
    """Baixar artigo baseado no DOI;

    Parâmetro:
        title: Título do artigo
        year: Ano do artigo
        doi: DOI do artigo

    """
    print('Realizando o download do arquivo "' + str(title) + '" do ano: ' + str(year) + '!')  # Informe o processamento
    url = 'https://link.springer.com/content/pdf/' + str(doi) + '.pdf'

    try:
        output = str(year) + ' - ' + str(title) + '.pdf'  # nome do artigo baixado (Year - Título)
        download(url, out=output)

    # Quando ocorrer problemas com caracteres especias, nomeio com o DOI.
    except:
        download(url)


def processar_resumos(arquivo):
    """Processar os resumos de artigos do site Springer Link com base em um arquivo.

    Parâmetro:
        arquivo: Nome de um arquivo .csv, inserido na mesma pasta do código, retirado do site Springer link
        baseado na busca da String.

    Retorno:
        lista_artigos: Retorna uma lista de artigos selecionados positivamente pela String.

    """

    df_urls = read_csv(arquivo)  # Leia um arquivo .csv e transforme em dataFrame.
    np_urls = array(df_urls[['Item Title', 'Publication Year', 'Item DOI', 'URL']])  # Transforme um pandas em numpy.
    tamanho_csv = len(np_urls)
    artigos = []

    for index in range(0, tamanho_csv):
        print('Processando o arquivo ' + str(index) + '!')  # Acompanhar o processo de analise.

        # Receba os dados do artigo: Title, Year, DOI e URL
        title = np_urls[index][0]
        year = np_urls[index][1]
        doi = np_urls[index][2]
        url = np_urls[index][3]

        """ Analise se o arquivo contém a String.
        Se sim, 
            * crie uma lista artigo e informe que foi selecionado (1);
            * insira na lista geral;
            * baixe o artigo.
        Se não, 
            * crie uma lista artigo e informe que não foi selecionado (0);
            * insina na lista geral.
        """
        resumo = coletar_resumo(url)

        if analisar_string(resumo):
            lista = [title, year, doi, url, resumo, 1]
            artigos.append(lista)
            baixar_artigo(title, year, doi)
        else:
            lista = [title, year, doi, url, resumo, 0]
            artigos.append(lista)

    return artigos


def salvar_lista_csv(artigos):
    """Salvar lista de artigos no formato CSV.
       Parâmetro:
           artigos: Lista de artigos processados.

    """
    pd_lista_doi = DataFrame(artigos, columns=['Title', 'Year', 'DOI', 'Link', 'Resumo', 'Status'])
    pd_lista_doi.to_csv('artigos_processados.csv', index=False)


# Execute as funções para processamento de arquivos;
# Informe o nome de acordo com o nome do seu arquivo 'SearchResults.csv'.
artigos = processar_resumos('SearchResults.csv')
salvar_lista_csv(artigos)
