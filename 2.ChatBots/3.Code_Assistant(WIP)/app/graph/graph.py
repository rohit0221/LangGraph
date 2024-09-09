from langchain_core.pydantic_v1 import BaseModel, Field

from langgraph.graph import END, StateGraph, START

from graph.conditional_edges import decide_to_finish
from graph.state import GraphState

from graph.nodes import generate,code_check,reflect
workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("generate", generate)  # generation solution
workflow.add_node("check_code", code_check)  # check code
workflow.add_node("reflect", reflect)  # reflect

# Build graph
workflow.add_edge(START, "generate")
workflow.add_edge("generate", "check_code")
workflow.add_conditional_edges(
    "check_code",
    decide_to_finish,
    {
        "end": END,
        "reflect": "reflect",
        "generate": "generate",
    },
)
workflow.add_edge("reflect", "generate")
app = workflow.compile()



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