import streamlit as st

class MessageHistory:
    """Class for controlling message history"""
    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def add_user_message(self, content):
        st.session_state.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content):
        st.session_state.messages.append({"role": "assistant", 
                                          "content": content})

    @property
    def messages(self):
        return st.session_state.messages
    
    def display(self):
        for message in self.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])