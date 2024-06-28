from dotenv import load_dotenv
import os
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from chains.retrieval_grader import *
from prompts.build_prompts import *

### Question Re-writer

# LLM
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

re_write_prompt = question_rewriter_prompt()


question_rewriter = re_write_prompt | llm | StrOutputParser()
