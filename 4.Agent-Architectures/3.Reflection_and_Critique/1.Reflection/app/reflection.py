from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage


def create_reflection_chain():
    llm = ChatOpenAI(model="gpt-4o-mini")
    reflection_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a teacher grading an essay submission. Generate critique and recommendations for the user's submission."
                " Provide detailed recommendations, including requests for length, depth, style, etc.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    reflect = reflection_prompt | llm    
    return reflect


def generate_reflection(request, generated_content):
    reflect= create_reflection_chain()
    reflection = ""
    for chunk in reflect.stream({"messages": [request, HumanMessage(content=generated_content)]}):
        print(chunk.content, end="")
        reflection += chunk.content

    return reflection