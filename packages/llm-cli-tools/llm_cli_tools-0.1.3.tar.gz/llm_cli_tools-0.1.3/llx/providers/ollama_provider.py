from ollama import chat
from collections.abc import AsyncIterator
from llx.providers.provider import Provider

class OllamaProvider(Provider):
    def __init__(self, model: str):
        self.model = model

    async def invoke(self, prompt: str, attachment: str=None) -> AsyncIterator[str]:
        stream = chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )

        for chunk in stream:
            yield chunk['message']['content']
