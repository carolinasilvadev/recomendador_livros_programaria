from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
import openai
from langchain_openai.chat_models import ChatOpenAI

client = MultiServerMCPClient(
    {
        "buscador_livros": {
            "command": "python",
            # Replace with absolute path to your math_server.py file
            "args": ["buscador.py"],
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
    while True:
            # try:
        user_input = input("> ")

        if user_input.lower() == "/q":
            break
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )
        print(response['messages'][-1].content)
            # except: 
            #      break

if __name__ == "__main__":
    asyncio.run(chat())