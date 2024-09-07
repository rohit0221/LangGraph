from langchain_core.messages import HumanMessage
from graph import graph, display_graph
import os
from dotenv import load_dotenv
load_dotenv()
import uuid
import asyncio


def generate_session_id() -> str:
    return str(uuid.uuid4())

async def print_final_generation(user_input):

    config = {"configurable": {"thread_id": generate_session_id()}}
    inputs = {
    "messages": [
        HumanMessage(
            content=user_input
        )
    ],
}

    async for event in graph.astream(inputs, config):
        print(event)


while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    display_graph(graph)
    asyncio.run(print_final_generation(user_input))