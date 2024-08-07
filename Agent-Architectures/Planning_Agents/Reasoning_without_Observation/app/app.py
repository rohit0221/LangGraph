
from dotenv import load_dotenv
import os
load_dotenv()

from graph.graph import create_graph, display_and_save_graph


app= create_graph()
display_and_save_graph(app)

def print_final_generation(inputs):
    for s in app.stream({"task": inputs}):
        print(s)
        print("---")


while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    print_final_generation(user_input) 