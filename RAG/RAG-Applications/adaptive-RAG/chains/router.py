from dotenv import load_dotenv
import os
load_dotenv()
from typing import Literal
from langchain_core.pydantic_v1 import BaseModel, Field

from prompts.build_prompts import build_route_prompt
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Build a Router to route the query to most relavant datasource
class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "web_search"] = Field(
        ...,
        description="Given a user question choose to route it to web search or a vectorstore.",
    )

route_prompt = build_route_prompt()
structured_llm_router = llm.with_structured_output(RouteQuery)

# Goes to web_search
question_router = route_prompt | structured_llm_router