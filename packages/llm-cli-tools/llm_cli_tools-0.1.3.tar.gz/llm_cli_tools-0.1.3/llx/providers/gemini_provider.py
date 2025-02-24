import os
from google import genai
from collections.abc import AsyncIterator
from llx.providers.provider import Provider

class GeminiProvider(Provider):
    def __init__(self, model: str):
        self.model = model
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.chat = client.chats.create(model=self.model)

    async def invoke(self, prompt: str, attachment: str=None) -> AsyncIterator[str]:
        response = self.chat.send_message_stream(prompt)
        for chunk in response:
            yield chunk.text
