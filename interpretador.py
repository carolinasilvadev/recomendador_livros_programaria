from mcp.server.fastmcp import FastMCP

mcp = FastMCP("interpretador_livros")

@mcp.tool()
def interpretar_input(frase: str) -> dict:
    """
    descrição:
    Interpreta uma frase do usuário e retorna os parâmetros estruturados
    para a busca de livros: gênero e número aproximado de páginas.

    Args:
        frase (str): entrada do usuário em linguagem natural.

    Returns:
        dict: {"genero": string, "numero_pg": int}
    """
    frase = frase.lower()

    generos_mapeados = {
        "romance": "romance",
        "comédia": "comedy",
        "engraçado": "comedy",
        "terror": "horror",
        "jogos": "Games",
        "astrologia": "Astrology",
        "poesia": "Poetry", 
        "quadrinhos": "Graphic Novels",
        "quadrinhos": "comics",
        "fantasia": "fantasy",
        "mistério": "mystery",
        "ficção científica": "science fiction",
        "aventura": "adventure",
    }

    tamanhos_mapeados = {
        "curto": 150,
        "pequeno": 150,
        "leve": 200,
        "médio": 300,
        "longo": 500,
        "grande": 500,
    }

    genero = "fiction"
    numero_pg = 300  # valor padrão

    for palavra, g in generos_mapeados.items():
        if palavra in frase:
            genero = g
            break

    for palavra, paginas in tamanhos_mapeados.items():
        if palavra in frase:
            numero_pg = paginas
            break

    return {"genero": genero, "numero_pg": numero_pg}


if __name__ == "__main__":
    mcp.run(transport="stdio")
