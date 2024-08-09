import os
from dotenv import load_dotenv
load_dotenv()

os.environ["LANGCHAIN_API_KEY"]=os.environ.get('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Hierarchical-Agent"
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

