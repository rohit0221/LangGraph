from typing import List

from typing_extensions import TypedDict

from graph.nodes import *
from graph.conditional_edges import *

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
    """

    question: str
    generation: str
    documents: List[str]


def create_graph_app():

    from langgraph.graph import END, StateGraph

    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("web_search", web_search_node)  # web search
    workflow.add_node("retrieve", retrieve_node)  # retrieve
    workflow.add_node("grade_documents", grade_documents_node)  # grade documents
    workflow.add_node("generate", generate_node)  # generatae
    workflow.add_node("transform_query", transform_query_node)  # transform_query

    # Set entry point
    workflow.set_conditional_entry_point(
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
    return app