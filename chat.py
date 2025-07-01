from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
import openai
from langchain_openai.chat_models import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()


buscador_path = Path(__file__).parent / "buscador.py"

client = MultiServerMCPClient(
    {   
        "buscador_livros": {
            "command": "python",
            "args": [str(Path(__file__).parent / "buscador.py")],
            "transport": "stdio",
        },
        "apify": {
            "transport": "sse",
            "url": "https://mcp.apify.com/sse?actors=runtime/goodreads-book-scraper",
            "headers": {
                "Authorization": f"Bearer {os.getenv('APIFY_API_KEY')}",
            }
        }
    }
)


OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

async def chat():
    llm = ChatOpenAI(name="o4-mini", top_p=0.5, api_key=openai.api_key)
    tools = await client.get_tools()
    agent = create_react_agent(
        model=llm,
        tools = tools,
        checkpointer= InMemorySaver(),
        prompt="Você é um agente que ajuda usuários a encontrar livros com base em suas solicitações. " \
        "Você pode usar tools para buscar informações sobre livros. Lembre-se de traduzir o gênero do livro para o inglês antes de fazer a busca na tool." \
        "Conside livros curtos os livros que tem no máximo 130 páginas." \
        "Considere livros longos os livros que tem mais de 400 páginas." \
        "Na hora de responder escolha os 5 melhores livros baseados nas avaliações dos usuários." \
        "Para encontrar informações de um livro específico, passe o nome em inglês, do jeito que o usuário escreveu e com codificação UTF-8 para a tool de buscar por nome." \
        "Se o usuário pesquisar livros com algum termo específico, use a ferramenta do goodreads-book-scraper do apify e passe o search term em inglês." 
    )

    print("Digite sua solicitação (ex: 'quero um romance curto'). Use /q para sair.\n")

    while True:
            # try:
        user_input = input("> ")

        if user_input.lower() == "/q":
            print("Saindo...")
            break

        config = {
            "configurable": {
                "thread_id": "1"
            }
            }

        # response = await agent.ainvoke(
        #     {"messages": [{"role": "user", "content": user_input}]}, config=config,
        # )

        async for chunk in agent.astream(
                        {"messages": user_input},
                        stream_mode=["messages", "custom"],
                        config=config,
                    ):
            print(chunk)
            import pdb
            pdb.set_trace()
        print("\nResposta do agente:\n")
        # print(response["messages"][-1].content)
        print("\n")
            # except: 
            #      print(f"Ocorreu um erro: {e}")
            #break

if __name__ == "__main__":
    asyncio.run(chat())