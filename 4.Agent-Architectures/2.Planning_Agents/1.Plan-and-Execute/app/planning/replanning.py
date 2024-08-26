from typing import Union
from langchain_core.pydantic_v1 import BaseModel, Field
from planning.planning import Plan
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from planning.planning_utils import create_prompt

class Response(BaseModel):
    """Response to user."""

    response: str


class Act(BaseModel):
    """Action to perform."""

    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
        "If you need to further use tools to get the answer, use Plan."
    )

def create_replanner(replanner_prompt,planning_llm):
    replanner = replanner_prompt | ChatOpenAI(
        model=planning_llm, temperature=0
    ).with_structured_output(Act)
    return replanner

replanner_prompt=create_prompt(task="replanning")
replanner=create_replanner(replanner_prompt,planning_llm="gpt-4o-mini")
