from dotenv import load_dotenv
import os
load_dotenv()

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from prompts.build_prompts import *

### Answer Grader

# Data model
class GradeAnswer(BaseModel):
    """Binary score to assess answer addresses question."""

    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )


answer_prompt = answer_grader_prompt()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm_answer_grader = llm.with_structured_output(GradeAnswer)

answer_grader = answer_prompt | structured_llm_answer_grader
