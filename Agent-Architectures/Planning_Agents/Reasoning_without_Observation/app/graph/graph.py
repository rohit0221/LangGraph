from graph.state import ReWOO
from graph.nodes import get_plan, _get_current_task
from agents_and_tools.tools import tool_execution, solve
from langgraph.graph import END, StateGraph, START


def display_and_save_graph(app, filename="graph.png"):
    from IPython.display import Image, display
    
    # Generate the graph image as a binary PNG data
    graph_image = app.get_graph(xray=True).draw_mermaid_png()
    
    # Save the image locally
    with open(filename, "wb") as f:
        f.write(graph_image)
    
    # Display the image (optional)
    display(Image(graph_image))

def _route(state):
    _step = _get_current_task(state)
    if _step is None:
        # We have executed all tasks
        return "solve"
    else:
        # We are still executing tasks, loop back to the "tool" node
        return "tool"
    
def create_graph():

    graph = StateGraph(ReWOO)
    graph.add_node("plan", get_plan)
    graph.add_node("tool", tool_execution)
    graph.add_node("solve", solve)
    graph.add_edge("plan", "tool")
    graph.add_edge("solve", END)
    graph.add_conditional_edges("tool", _route)
    graph.add_edge(START, "plan")

    app = graph.compile()
    return app

