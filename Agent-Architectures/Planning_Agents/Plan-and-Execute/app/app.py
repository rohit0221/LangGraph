from dotenv import load_dotenv
import os
load_dotenv()

from graph.graph import create_graph, display_and_save_graph

app= create_graph()
display_and_save_graph(app)

import asyncio

async def print_final_generation(user_input):
    config = {"recursion_limit": 50}
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

