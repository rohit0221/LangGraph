from langgraph.graph import StateGraph, START, END
from graph.nodes import PlanExecute, plan_step, replan_step, execute_step, should_end


# def display_graph(app):
#     from IPython.display import Image, display
#     display(Image(app.get_graph(xray=True).draw_mermaid_png()))

def display_and_save_graph(app, filename="graph.png"):
    from IPython.display import Image, display
    
    # Generate the graph image as a binary PNG data
    graph_image = app.get_graph(xray=True).draw_mermaid_png()
    
    # Save the image locally
    with open(filename, "wb") as f:
        f.write(graph_image)
    
    # Display the image (optional)
    display(Image(graph_image))

# Usage example:
# display_and_save_graph(app, "output_graph.png")


def create_graph():
    workflow = StateGraph(PlanExecute)

    # Add the plan node
    workflow.add_node("planner", plan_step)

    # Add the execution step
    workflow.add_node("agent", execute_step)

    # Add a replan node
    workflow.add_node("replan", replan_step)

    workflow.add_edge(START, "planner")

    # From plan we go to agent
    workflow.add_edge("planner", "agent")

    # From agent, we replan
    workflow.add_edge("agent", "replan")

    workflow.add_conditional_edges(
        "replan",
        # Next, we pass in the function that will determine which node is called next.
        should_end,
        ["agent", END],
    )

    # Finally, we compile it!
    # This compiles it into a LangChain Runnable,
    # meaning you can use it as you would any other runnable
    app = workflow.compile()

    return app