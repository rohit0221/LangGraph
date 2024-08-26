from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from typing import List
from planning.planning_utils import create_prompt

class Plan(BaseModel):
    """Plan to follow in future"""

    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )

def create_planner(planner_prompt,planning_llm):
    planner = planner_prompt | ChatOpenAI(
        model=planning_llm, temperature=0
    ).with_structured_output(Plan)
    return planner


# Create the planner
planner_prompt=create_prompt(task="planning")
planner=create_planner(planner_prompt,planning_llm="gpt-4o-mini")


