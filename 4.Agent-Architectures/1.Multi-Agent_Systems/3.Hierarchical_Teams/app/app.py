import os
from dotenv import load_dotenv
load_dotenv()

from graphs.super_graph import create_supergraph, display_and_save_graph
os.environ["LANGCHAIN_API_KEY"]=os.environ.get('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Hierarchical-Agent"
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")



app= create_supergraph()
display_and_save_graph(app)

import asyncio

async def print_final_generation(user_input):
    config = {"recursion_limit": 100}
    inputs = {"input": user_input}

    async for event in app.astream(inputs, config=config):
        for k, v in event.items():
            if k != "__end__":
                print(v)
# asyncio.run(print_final_generation())

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    
    asyncio.run(print_final_generation(user_input))



