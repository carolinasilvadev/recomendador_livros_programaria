import pandas as pd 
from mcp.server.fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("buscador_livros")

base_livros = Path(__file__).parent / "GoodReads_100k_books.csv"

@mcp.tool()
def buscador(genero, numero_pg):
    """
    descricao: 
    Função para buscar livros dentro de uma base de dados
    a partir de um genero e numero de páginas. 
    Importante que genero seja passado em inglês. 

    Args:
        genero (string): nome do genero (inglês)
        numero_pg (int): numero de paginas do livro

    Returns:
        dataframe: livros encontrados com as colunas: 
         'author', 'bookformat', 'desc', 'genre', 'img', 'isbn', 'isbn13',
       'link', 'pages', 'rating', 'reviews', 'title', 'totalratings'
    """   

    base = pd.read_csv(base_livros)
    print('entrou aqui')
    base['pages'] = base['pages'].astype(int)
    base['rating'] = base['rating'].astype(float)
    base = base[(base['genre'].str.contains(genero, case=False)) & ((numero_pg-20)<base['pages']) & (base['pages']<(numero_pg+20))]

    if len(base)>100:
        base_4 = base[base['rating']>4]
        if len(base_4) >0:
            base = base_4

    base = base.sort_values(by="rating", ascending=False)
    resultado = base[['title', 'author', 'pages', 'genre', 'rating', 'desc']].head(10).to_dict(orient='records')

    return resultado


if __name__ == "__main__":
    mcp.run(transport="stdio")