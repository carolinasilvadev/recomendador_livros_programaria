from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
import openai
from langchain_openai.chat_models import ChatOpenAI
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
    }
)


OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

async def chat():
    llm = ChatOpenAI(name="o4-mini", top_p=0.5, api_key=openai.api_key)
    tools = await client.get_tools()
    agent = create_react_agent(
        model=llm,
        tools = tools,
        prompt="Você é um agente que ajuda usuários a encontrar livros com base em suas solicitações. " \
        "Você pode usar tools para buscar informações sobre livros. Lembre-se de traduzir o gênero do livro para o inglês antes de fazer a busca na tool." \
        "Conside livros curtos os livros que tem no máximo 130 páginas." \
        "Considere livros longos os livros que tem mais de 400 páginas." \
        "Na hora de responder escolha os 5 melhores livros baseados nas avaliações dos usuários." \
        "Para encontrar informações de um livro específico, passe o nome em inglês e com codificação UTF-8." \
    )

    print("Digite sua solicitação (ex: 'quero um romance curto'). Use /q para sair.\n")

    while True:
            # try:
        user_input = input("> ")

        if user_input.lower() == "/q":
            print("Saindo...")
            break

        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )

        # async for chunk in agent.astream(
        #                 {"messages": user_input},
        #                 stream_mode=["messages", "custom"],
        #             ):
        #     print(chunk)
        #     import pdb
        #     pdb.set_trace()
        print("\nResposta do agente:\n")
        print(response["messages"][-1].content)
        print("\n")
            # except: 
            #      print(f"Ocorreu um erro: {e}")
            #break

if __name__ == "__main__":
    asyncio.run(chat())