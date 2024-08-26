from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from generation import create_generate_chain
from reflection import create_reflection_chain
from typing import List, Sequence


async def generation_node(state: Sequence[BaseMessage]):
    generate = create_generate_chain()
    return await generate.ainvoke({"messages": state})


async def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    reflect = create_reflection_chain()
    # Other messages we need to adjust
    cls_map = {"ai": HumanMessage, "human": AIMessage}
    # First message is the original user request. We hold it the same for all nodes
    translated = [messages[0]] + [
        cls_map[msg.type](content=msg.content) for msg in messages[1:]
    ]
    res = await reflect.ainvoke({"messages": translated})
    # We treat the output of this as human feedback for the generator
    return HumanMessage(content=res.content)