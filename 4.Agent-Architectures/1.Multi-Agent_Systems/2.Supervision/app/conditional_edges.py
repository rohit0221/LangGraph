from state import State
from langgraph.graph import END, StateGraph, START

def should_continue(state: State):
    if len(state["messages"]) > 6:
        # End after 3 iterations
        return END
    return "reflect"