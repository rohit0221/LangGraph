from langgraph.checkpoint.memory import MemorySaver
from state import State
from nodes import generation_node,reflection_node
from conditional_edges import should_continue

from langgraph.graph import END, StateGraph, START


builder = StateGraph(State)
builder.add_node("generate", generation_node)
builder.add_node("reflect", reflection_node)

builder.add_edge(START, "generate")




builder.add_conditional_edges("generate", should_continue)
builder.add_edge("reflect", "generate")
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

def display_graph(graph, file_path="graph_output.png"):
    from IPython.display import Image, display

    try:
        # Generate the graph as a PNG image
        graph_image = graph.get_graph(xray=True).draw_mermaid_png()

        # Save the image to disk
        with open(file_path, "wb") as f:
            f.write(graph_image)

        # Display the graph in the notebook
        display(Image(graph_image))
        
    except Exception as e:
        print(f"An error occurred: {e}")