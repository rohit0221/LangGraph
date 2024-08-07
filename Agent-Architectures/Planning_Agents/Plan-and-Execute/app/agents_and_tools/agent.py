from langchain import hub
from langchain_openai import ChatOpenAI

from agents_and_tools.tools import tools
from langgraph.prebuilt import create_react_agent


# Get the prompt to use - you can modify this!
prompt = hub.pull("wfh/react-agent-executor")
prompt.pretty_print()

# Choose the LLM that will drive the agent
llm = ChatOpenAI(model="gpt-4o-mini")


agent_executor = create_react_agent(llm, tools, messages_modifier=prompt)