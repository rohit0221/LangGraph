from typing_extensions import TypedDict
from typing import Annotated, List, Sequence
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]