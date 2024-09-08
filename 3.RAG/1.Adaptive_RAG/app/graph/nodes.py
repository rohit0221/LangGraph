import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.tools.tavily_search import TavilySearchResults

web_search_tool = TavilySearchResults(k=3)

from langchain.schema import Document
from utils.indexer import build_retriever
from chains.question_rewriter import *
from chains.retrieval_grader import *
from chains.hullucination_grader import *
from chains.answer_grader import *
from chains.response_generator import *

def retrieve(state):
    """
    Retrieve documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["question"]
    retriever=build_retriever()

    # Retrieval
    documents = retriever.invoke(question)
    # Update the state with retrieved documents while retaining other existing state keys
    state["documents"] = documents
    return state


def generate(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updated state with LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    # RAG generation
    generation = rag_chain.invoke({"context": documents, "question": question})

    # Update the state with the new generation while retaining other existing state keys
    state["generation"] = generation
    return state


def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updated state with only filtered relevant documents
    """
    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]
    
    # Score each document
    filtered_docs = []
    for d in documents:
        score = retrieval_grader_chain.invoke(
            {"question": question, "document": d.page_content}
        )
        grade = score.binary_score
        if grade == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            continue

    # Update the state with filtered documents while retaining other existing state keys
    state["documents"] = filtered_docs
    return state

def transform_query(state):
    """
    Transform the query to produce a better question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updated state with a rephrased question
    """

    print("---TRANSFORM QUERY---")
    question = state["question"]

    # Re-write the question
    better_question = question_rewriter_chain.invoke({"question": question})

    # Update the state with the rephrased question while retaining other existing state keys
    state["question"] = better_question
    return state



def web_search(state):
    """
    Web search based on the rephrased question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updated state with web search results appended to documents
    """

    print("---WEB SEARCH---")
    question = state["question"]

    # Web search
    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    web_results_doc = Document(page_content=web_results)

    # Initialize documents if not already done
    if "documents" not in state or state["documents"] is None:
        state["documents"] = []

    # Append web results to existing documents
    state["documents"].append(web_results_doc)

    return state

