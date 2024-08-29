from langchain_openai import ChatOpenAI


### Generate

from langchain import hub
from langchain_core.output_parsers import StrOutputParser

# def generate_response(question,vectorstore):
        
# Prompt
prompt = hub.pull("rlm/rag-prompt")

# LLM
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Chain
rag_chain = prompt | llm | StrOutputParser()

