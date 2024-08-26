from dotenv import load_dotenv
import os
load_dotenv()


from graph.app_graph import create_graph_app

graph = create_graph_app()

def print_final_generation(inputs):
        
    import pprint

    inputs = {
        "messages": [
            ("user", user_input),
        ]
    }
    for output in graph.stream(inputs):
        for key, value in output.items():
            pprint.pprint(f"Output from node '{key}':")
            pprint.pprint("---")
            pprint.pprint(value, indent=2, width=80, depth=None)
        pprint.pprint("\n---\n")


# input = input("Please enter your question: ")
# print_final_generation(input)

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    print_final_generation(user_input)
