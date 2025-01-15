import streamlit as st
import logging
from dotenv import load_dotenv
import os

from openai_ext import OpenAI
from message_history import MessageHistory
from api_key import ApiKey

class ChatApp:
    """Main class that controls app behaviour"""
    def __init__(self):
        self.api_keys = {
            "OPENAI": ApiKey().openai
        }
      
        self.message_history = MessageHistory()

        # Set window and chat titles
        st.set_page_config(page_title="Chat BOT")
        st.title("Helpfull assistant")

        self.sidebar = st.sidebar
        # Current LLM model
        self.model = self.sidebar.selectbox(
            "Model",
            ["gpt-4o-mini", "gpt-4o"],
            index=0,
            placeholder="Please select model...",
            label_visibility="hidden"
        )

        # Config loggins
        logging.basicConfig(level=logging.INFO)

    def _assistant_response(self, messages):
        """
        Return assistant response based on selected model and previous chat history
        """
        try:
            with st.spinner("Contemplating..."):
                client = OpenAI(api_key=self.api_keys["OPENAI"],
                                model=self.model)
                # Stream chat response from the model
                stream = client.stream_chat(messages)

            # Display assistant response in chat message container
            response = st.write_stream(stream)
            logging.info(f"Response: {response}")
            return response
        except Exception as e:
            # Log if any errors occur while streaming
            logging.info(f"Streeming error: {str(e)}")
            raise e
        
    def run_app(self):
        """Starts app"""
        logging.info("App started")
        logging.info(f"Model selected: {self.model}")

        if len(self.message_history.messages) == 0:
            self.message_history.add_assistant_message("How can I help you?")

        self.message_history.display()
        
        # Promt for user input and add it to chat history
        if promt := st.chat_input("Your promt"):
            self.message_history.add_user_message(promt)

            with st.chat_message("user"):
                st.markdown(promt)
            logging.info(f"Promt: {promt}")

            # Generate a new response if the last message is not from assistant
            if self.message_history.messages[-1]["role"] != "assistant":
                with st.chat_message("assistant").empty():
                    try:
                        # Prepare message history for the promt
                        messages = self.message_history.messages[:]
                        # Stream response from assistant
                        response = self._assistant_response(messages)
                        self.message_history.add_assistant_message(response)
                    except Exception as e:
                        # Handle and display an error message
                        st.error("An error occured while generating response.")
                        logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    ca = ChatApp()
    ca.run_app()