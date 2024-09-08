from graph.state import GraphState

from graph.nodes import *
from graph.conditional_edge_functions import *
from langgraph.graph import END,START, StateGraph

import os
from dotenv import load_dotenv
load_dotenv()

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("web_search", web_search)  # web search
workflow.add_node("retrieve", retrieve)  # retrieve
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generatae
workflow.add_node("transform_query", transform_query)  # transform_query

# Build graph
workflow.add_conditional_edges(
    START,
    route_question,
    {
        "web_search": "web_search",
        "vectorstore": "retrieve",
    },
)


# Build Edges point
workflow.add_edge("web_search", "generate")
workflow.add_edge("retrieve", "grade_documents")   
workflow.add_edge("transform_query", "retrieve")

workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
    },
)

workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "transform_query",
    },
)

# Compile
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
