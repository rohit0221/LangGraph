from langgraph.graph import END, StateGraph, START
from langchain_core.messages import HumanMessage

from agents.research_team import search_node, research_node, supervisor_agent, ResearchTeamState

def create_research_chain():
        
    research_graph = StateGraph(ResearchTeamState)
    research_graph.add_node("Search", search_node)
    research_graph.add_node("WebScraper", research_node)
    research_graph.add_node("supervisor", supervisor_agent)

    # Define the control flow
    research_graph.add_edge("Search", "supervisor")
    research_graph.add_edge("WebScraper", "supervisor")
    research_graph.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {"Search": "Search", "WebScraper": "WebScraper", "FINISH": END},
    )


    research_graph.add_edge(START, "supervisor")
    chain = research_graph.compile()


    # The following functions interoperate between the top level graph state
    # and the state of the research sub-graph
    # this makes it so that the states of each graph don't get intermixed
    def enter_chain(message: str):
        results = {
            "messages": [HumanMessage(content=message)],
        }
        return results


    research_chain = enter_chain | chain

    return research_chain