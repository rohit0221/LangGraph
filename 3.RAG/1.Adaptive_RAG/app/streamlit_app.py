from dotenv import load_dotenv
import streamlit as st

import os
load_dotenv()

from graph.app_graph import create_graph_app

from pprint import pprint


app = create_graph_app()

# def print_final_generation(inputs):
        
#     # Run
#     # inputs = {"question": "What are the types of agent memory?"}
#     for output in app.stream(inputs):
#         for key, value in output.items():
#             # Node
#             pprint(f"Node '{key}':")
#             # Optional: print full state at each node
#             # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
#         pprint("\n---\n")
#     # Final generation
#     pprint(value["generation"])


def print_final_generation(inputs):
    # Stream outputs from the app
    inputs = {"question": inputs}
    for output in app.stream(inputs):
        # For each node in the output, yield the formatted string
        for key, value in output.items():
            # Create a formatted string for the node
            node_output = f"Node '{key}':"
            yield node_output  # Yield the node output
            
            # Optionally yield full state at each node
            # keys_output = pprint.pformat(value["keys"], indent=2, width=80, depth=None)
            # yield keys_output

        # Yield a separator between nodes
        yield "\n---\n"

    # Yield the final generation
    final_generation = value.get("generation", "No generation found")
    yield final_generation


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
        placeholder = st.empty()

        if user_question:                                             
            st.session_state.messages.append({"role": "user", "content": user_question})
            streamed_output = ""

            # Use the modified print_final_generation function to stream the answer
            for partial_answer in print_final_generation(user_question):
                # Accumulate the streamed output
                streamed_output += partial_answer + "\n"
                
                # Update the placeholder with the current streamed content
                placeholder.text(streamed_output)
            
            # Once streaming is complete, add the final streamed output to the session state
            st.session_state.messages.append({"role": "assistant", "content": streamed_output})
            
            # Display the final message in the chat format
            st.chat_message("assistant", avatar="./bot.png").write(streamed_output)
    
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