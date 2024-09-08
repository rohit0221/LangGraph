from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
import streamlit as st
import os
from graph.app_graph import app, display_graph
from dotenv import load_dotenv

load_dotenv()

def clear_submit():
    """
    Clear the Submit Button State
    """
    st.session_state["submit"] = False

st.set_page_config(page_title="LangChain: Chat with pandas DataFrame", page_icon="🦜")
st.title("🦜 LangChain: Chat with pandas DataFrame")

openai_api_key = os.environ.get('OPENAI_API_KEY')

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What is this data about?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    llm = ChatOpenAI(
        temperature=0, model="gpt-4o-mini", openai_api_key=openai_api_key, streaming=True
    )

    # Create a placeholder for the assistant's message
    message_placeholder = st.chat_message("assistant").empty()

    # Create an empty container for the response
    response_container = st.empty()

    try:
        # Consume the streaming response from the app
        response_text = ""
        for response in app.stream(st.session_state.messages):
            # Append new content to the response text
            response_text += response

            # Update the placeholder with the new response content
            message_placeholder.write(response_text)
        
        # Once the response is complete, store it in the session state
        st.session_state.messages.append({"role": "assistant", "content": response_text})

    except TypeError as e:
        response_text = f"Error occurred: {e}"
        message_placeholder.write(response_text)
