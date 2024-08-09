from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage


def create_generate_chain():
        
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an essay assistant tasked with writing excellent 1-paragraph essays."
                " Generate the best essay possible for the user's request."
                " Keep the essay within 200 words "
                " If the user provides critique, respond with a revised version of your previous attempts.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    llm = ChatOpenAI(model="gpt-4o-mini")

    generate = prompt | llm

    return generate


def generate_essay(content):
    generate = create_generate_chain()
    essay = ""
    request = HumanMessage(
        content=content
    )
    for chunk in generate.stream({"messages": [request]}):
        print(chunk.content, end="")
        essay += chunk.content

    return essay
    