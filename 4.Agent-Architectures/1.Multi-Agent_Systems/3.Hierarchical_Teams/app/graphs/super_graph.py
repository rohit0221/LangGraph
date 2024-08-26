from langgraph.graph import END, StateGraph, START
from typing import Annotated, List
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
import operator

from graphs.research_subgraph import create_research_chain
from graphs.documentation_subgraph import create_authoring_chain

from langchain_core.messages import BaseMessage
from langchain_openai.chat_models import ChatOpenAI
from agents.agent_utils import create_team_supervisor

llm = ChatOpenAI(model="gpt-4o-mini")


authoring_chain = create_authoring_chain()
create_research_chain = create_research_chain()

def display_and_save_graph(app, filename="graph.png"):
    from IPython.display import Image, display
    
    # Generate the graph image as a binary PNG data
    graph_image = app.get_graph(xray=True).draw_mermaid_png()
    
    # Save the image locally
    with open(filename, "wb") as f:
        f.write(graph_image)
    
    # Display the image (optional)
    display(Image(graph_image))
    
def create_supergraph():
        
    supervisor_node = create_team_supervisor(
        llm,
        "You are a supervisor tasked with managing a conversation between the"
        " following teams: {team_members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When finished,"
        " respond with FINISH.",
        ["ResearchTeam", "PaperWritingTeam"],
    )

    # Top-level graph state
    class State(TypedDict):
        messages: Annotated[List[BaseMessage], operator.add]
        next: str


    def get_last_message(state: State) -> str:
        return state["messages"][-1].content


    def join_graph(response: dict):
        return {"messages": [response["messages"][-1]]}


    # Define the graph.
    super_graph = StateGraph(State)
    # First add the nodes, which will do the work
    super_graph.add_node("ResearchTeam", get_last_message | research_chain | join_graph)
    super_graph.add_node(
        "PaperWritingTeam", get_last_message | authoring_chain | join_graph
    )
    super_graph.add_node("supervisor", supervisor_node)

    # Define the graph connections, which controls how the logic
    # propagates through the program
    super_graph.add_edge("ResearchTeam", "supervisor")
    super_graph.add_edge("PaperWritingTeam", "supervisor")
    super_graph.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "PaperWritingTeam": "PaperWritingTeam",
            "ResearchTeam": "ResearchTeam",
            "FINISH": END,
        },
    )
    super_graph.add_edge(START, "supervisor")
    super_graph = super_graph.compile()
    
    return super_graph