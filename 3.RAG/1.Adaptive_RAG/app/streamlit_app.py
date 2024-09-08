from dotenv import load_dotenv
import streamlit as st

import os
load_dotenv()

from graph.app_graph import app

from pprint import pprint



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
            # Add the user question to the session state
            st.session_state.messages.append({"role": "user", "content": user_question})

            # Initialize the assistant's message with the avatar
            assistant_message = st.chat_message("assistant", avatar="./bot.png")

            # Initialize an empty list to keep track of already processed nodes
            processed_nodes = set()

            # Use the modified print_final_generation function to stream the answer
            streamed_output = ""  # Accumulate the full streamed output here

            # Stream the answer progressively
            for partial_answer in print_final_generation(user_question):
                # Check if the partial answer is a node or part of the expected structure
                if partial_answer.startswith("Node"):
                    # If the node has not been processed yet, add to the output
                    node_name = partial_answer.split("'")[1]  # Extract node name
                    if node_name not in processed_nodes:
                        processed_nodes.add(node_name)
                        streamed_output += partial_answer + "\n"

                else:
                    # For other outputs, just add them directly
                    streamed_output += partial_answer + "\n"
                
                # Update the assistant's message with the accumulated streamed output
                assistant_message.markdown(streamed_output)

            # Once streaming is complete, add the final streamed output to the session state
            st.session_state.messages.append({"role": "assistant", "content": streamed_output})
    
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