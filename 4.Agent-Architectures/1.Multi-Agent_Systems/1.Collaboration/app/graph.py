
from state import AgentState
from nodes import *
from langgraph.graph import END, StateGraph

from router import router

def create_graph():

    research_node=create_research_node()
    chart_node = create_chart_node()
    tool_node= create_tool_node()
        
    workflow = StateGraph(AgentState)
    workflow.add_node("Researcher", research_node)
    workflow.add_node("chart_generator", chart_node)
    workflow.add_node("call_tool", tool_node)

    workflow.add_conditional_edges(
        "Researcher",
        router,
        {"continue": "chart_generator", "call_tool": "call_tool", "__end__": END},
    )
    workflow.add_conditional_edges(
        "chart_generator",
        router,
        {"continue": "Researcher", "call_tool": "call_tool", "__end__": END},
    )

    workflow.add_conditional_edges(
        "call_tool",
        # Each agent node updates the 'sender' field
        # the tool calling node does not, meaning
        # this edge will route back to the original agent
        # who invoked the tool
        lambda x: x["sender"],
        {
            "Researcher": "Researcher",
            "chart_generator": "chart_generator",
        },
    )
    workflow.set_entry_point("Researcher")
    graph = workflow.compile()

    return graph


def display_graph(graph):
    
    from IPython.display import Image, display

    try:
        display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
    except Exception:
        # This requires some extra dependencies and is optional
        pass


