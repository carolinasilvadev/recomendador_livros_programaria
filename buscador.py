import pandas as pd 
from mcp.server.fastmcp import FastMCP
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

mcp = FastMCP("buscador_livros")

base_livros = Path(__file__).parent / "GoodReads_100k_books.csv"

@mcp.tool()
def buscador(genero: str, numero_pg: int) -> pd.DataFrame:
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

    base = pd.read_csv(base_livros, encoding= 'utf-8')
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

@mcp.tool()
def buscar_por_nome(titulo: str):
    """
    descricao: 
    Função para buscar as informações de um 
    livro dentro de uma base de dados
    a partir do nome dele. 
    Importante que o nome do livro seja passado em inglês. 

    Args:
        title (string): nome do livro (inglês)

    Returns:
        dict: informações do livro: 
        author: The name of the author/authors of the book
        bookformat: The format of the book
        desc: The description of the book
        genre: The list of genres related to the book
        img: Image link of the book
        isbn: ISBN code of the book
        isbn13: ISBN13 code of the book
        link: The goodreads links of the book
        pages: Number of pages in the book
        rating: Average rating of the book
        reviews: The number of reviews the book has
        title: The title of the book
        totalratings: Totalratings of the book
    """   
    base = pd.read_csv(base_livros, encoding= 'utf-8')

    base = base[base['title'].str.contains(titulo, case=False, na=False)]

    return base


if __name__ == "__main__":
    mcp.run(transport="stdio")