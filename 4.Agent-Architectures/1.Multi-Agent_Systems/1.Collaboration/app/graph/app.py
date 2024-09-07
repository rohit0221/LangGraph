
from langchain_core.messages import HumanMessage
from graph import graph, display_graph


def print_final_generation(inputs):
    #inputs = {"question": inputs}


    events = graph.stream(
        {
            "messages": [
                HumanMessage(
                    content=inputs
                )
            ],
        },
        # Maximum number of steps to take in the graph
        {"recursion_limit": 150},
    )
    for s in events:
        print(s)
        print("----")

# input = input("Please enter your question: ")
# print_final_generation(input)

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    display_graph(graph)
    print_final_generation(user_input)        