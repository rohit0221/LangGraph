from dotenv import load_dotenv
import os
load_dotenv()
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
from langchain_core.pydantic_v1 import BaseModel, Field

from prompts.build_prompts import *

### Hallucination Grader

# Data model
class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: str = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )

hallucination_prompt=build_hullucination_grader_prompt()
structured_llm_hullucination_grader = llm.with_structured_output(GradeHallucinations)


hallucination_grader = hallucination_prompt | structured_llm_hullucination_grader