from langchain_openai import ChatOpenAI



from planning.planning_utils import create_prompt



 
import re

from langchain_core.prompts import ChatPromptTemplate

def create_planner():
    model = ChatOpenAI(model="gpt-4o-mini",temperature=0)
    # Regex to match expressions of the form E#... = ...[...]
    task="planner"
    prompt_template = create_prompt(task)
    planner = prompt_template | model
    return planner
