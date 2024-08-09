from dotenv import load_dotenv
import os
load_dotenv()

os.environ["LANGCHAIN_API_KEY"]=os.environ.get('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Basic-Reflection"
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from graph import create_graph, display_and_save_graph
llm = ChatOpenAI(model="gpt-4o-mini")


app= create_graph()
display_and_save_graph(app)

import asyncio

async def print_final_generation(user_input):

    async for event in app.astream(
        [
            HumanMessage(
                content=user_input
            )
        ],
    ):
        print(event)
        print("---")
# asyncio.run(print_final_generation())

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    
    asyncio.run(print_final_generation(user_input))





