from dotenv import load_dotenv
import streamlit as st

import os
load_dotenv()

from graph.app_graph import create_graph_app

from pprint import pprint


app = create_graph_app()

def print_final_generation(inputs):
        
    # Run
    # inputs = {"question": "What are the types of agent memory?"}
    for output in app.stream(inputs):
        for key, value in output.items():
            # Node
            pprint(f"Node '{key}':")
            # Optional: print full state at each node
            # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
        pprint("\n---\n")
    # Final generation
    pprint(value["generation"])


def handle_message():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Bring it on!"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"],avatar="./bot.png").write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user",avatar="./human2.png").write(prompt)
        print(prompt)
        print(type(prompt))

        message=st.session_state.messages
        print(message)
        print(type(message))
        user_question = next((item['content'] for item in reversed(message) if item['role'] == 'user'), None)

        if user_question:
            answer=print_final_generation(user_question)                                                
            st.session_state.messages.append({"role": "user", "content": user_question})
            print(answer)
            print(type(answer))
            msg = answer['output_text']
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant",avatar="./bot.png").write(msg)
    
def main():

    from PIL import Image
    # Loading Image using PIL
    im = Image.open('./bot.png')
    # Adding Image to web app
    st.set_page_config(page_title="ActixOne ChatBot", page_icon = im)

    #st.set_page_config("Chat PDF")
    st.image("./title.PNG", width=400)
    st.header("Welcome to Adaptive RAG")
    st.image("./bot.PNG", width=100)
    handle_message()


if __name__ == "__main__":
    main()