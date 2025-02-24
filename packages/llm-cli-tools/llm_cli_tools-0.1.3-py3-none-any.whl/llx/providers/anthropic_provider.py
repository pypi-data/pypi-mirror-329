import os
import base64
import anthropic
from collections.abc import Iterator, AsyncIterator
from llx.providers.provider import Provider

class AnthropicProvider(Provider):
    def __init__(self, model):
        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def invoke(self, prompt: str, attachment: str=None) -> AsyncIterator[str]:        
        with self.client.messages.stream(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        ) as stream:
            for chunk in stream.text_stream:
                yield chunk
