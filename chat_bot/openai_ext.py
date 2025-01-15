from openai import OpenAI

class OpenAI(OpenAI):
    """Extends OpenAI class with stream_chat method"""
    def __init__(self, *, api_key, model):
        super().__init__(api_key=api_key)
        self.model=model

    def stream_chat(self, messages):
        """Return stream response from OpenAI"""
        stream = self.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        )
        return stream