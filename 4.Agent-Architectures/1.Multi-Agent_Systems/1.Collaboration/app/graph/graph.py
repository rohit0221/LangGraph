from state import AgentState
from nodes import *
from langgraph.graph import END,START, StateGraph
from conditional_edge_router_function import router


    
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
workflow.add_edge(START, "Researcher")
graph = workflow.compile()



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



