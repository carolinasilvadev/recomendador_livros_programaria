from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
import openai
from langchain_openai.chat_models import ChatOpenAI
from pathlib import Path

buscador_path = Path(__file__).parent / "buscador.py"

client = MultiServerMCPClient(
    {
        "interpretador_livros": {
            "command": "python",
            "args": [str(Path(__file__).parent / "interpretador.py")],
            "transport": "stdio",
        },
        "buscador_livros": {
            "command": "python",
            "args": [str(Path(__file__).parent / "buscador.py")],
            "transport": "stdio",
        },
    }
)




async def chat():
    tools = await client.get_tools()
    agent = create_react_agent(
        model=llm,
        tools = tools
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
        print("\nResposta do agente:\n")
        print(response['messages'][-1].content)
        print("\n")
            # except: 
            #      print(f"Ocorreu um erro: {e}")
            #break

if __name__ == "__main__":
    asyncio.run(chat())