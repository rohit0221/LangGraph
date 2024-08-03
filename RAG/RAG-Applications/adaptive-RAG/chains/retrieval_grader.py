from dotenv import load_dotenv
import os
load_dotenv()

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
from prompts.build_prompts import *
from chains.indexer import *

### Retrieval Grader
# Data model
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )

grade_prompt = build_grader_prompt()
structured_llm_grader = llm.with_structured_output(GradeDocuments)


retrieval_grader = grade_prompt | structured_llm_grader