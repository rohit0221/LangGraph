from typing import List, Sequence

from langgraph.graph import END, MessageGraph, START
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from nodes import generation_node, reflection_node


def display_and_save_graph(app, filename="graph.png"):
    from IPython.display import Image, display
    
    # Generate the graph image as a binary PNG data
    graph_image = app.get_graph(xray=True).draw_mermaid_png()
    
    # Save the image locally
    with open(filename, "wb") as f:
        f.write(graph_image)
    
    # Display the image (optional)
    display(Image(graph_image))
    
def create_graph():
    builder = MessageGraph()
    builder.add_node("generate", generation_node)
    builder.add_node("reflect", reflection_node)
    builder.add_edge(START, "generate")

    def should_continue(state: List[BaseMessage]):
        if len(state) > 6:
            # End after 3 iterations
            return END
        return "reflect"

    builder.add_conditional_edges("generate", should_continue)
    builder.add_edge("reflect", "generate")
    graph = builder.compile()

    return graph