
import functools
from langchain_core.messages import AIMessage
from langchain_core.messages import ToolMessage
from langchain_openai import ChatOpenAI
from agent import create_agent
from tools import tavily_tool, python_repl
llm = ChatOpenAI(model="gpt-4o-mini")

# Helper function to create a node for a given agent
def agent_node(state, agent, name):
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        # Since we have a strict workflow, we can
        # track the sender so we know who to pass to next.
        "sender": name,
    }




def create_tool_node():
    from langgraph.prebuilt import ToolNode
    tools = [tavily_tool, python_repl]
    tool_node = ToolNode(tools)

    return tool_node

def create_chart_node():
    chart_agent = create_agent(
        llm,
        [python_repl],
        system_message="Any charts you display will be visible by the user.",
    )
    chart_node = functools.partial(agent_node, agent=chart_agent, name="chart_generator")

    return chart_node

def create_research_node():
    research_agent = create_agent(
    llm,
    [tavily_tool],
    system_message="You should provide accurate data for the chart_generator to use.",
)
    research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

    return research_node

