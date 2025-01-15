from dotenv import load_dotenv
import os

class ApiKey():
    def __init__(self):
        load_dotenv()

    @property
    def openai(self):
        return os.environ.get("OPENAI_API_KEY")