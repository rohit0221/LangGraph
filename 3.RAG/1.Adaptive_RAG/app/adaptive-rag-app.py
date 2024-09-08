from dotenv import load_dotenv
import os
load_dotenv()

from graph.app_graph import app,display_graph

from pprint import pprint



def print_final_generation(inputs):
        
    # Run
    # inputs = {"question": "What are the types of agent memory?"}
    inputs = {"question": inputs}
    print("the input from user is :::::")
    print(inputs)
    for output in app.stream(inputs):
        for key, value in output.items():
            # Node
            pprint(f"Node '{key}':")
            # Optional: print full state at each node
            # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
        pprint("\n---\n")
    # Final generation
    pprint(value["generation"])


# input = input("Please enter your question: ")
# print_final_generation(input)

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    display_graph(app)
    print_final_generation(user_input)
    
