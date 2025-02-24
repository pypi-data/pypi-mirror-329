from collections.abc import Iterator
from enum import Enum
import os
from llx.providers.openai_provider import OpenAIProvider
from llx.providers.ollama_provider import OllamaProvider
from llx.providers.anthropic_provider import AnthropicProvider
from llx.providers.deepseek_provider import DeepseekProvider
from llx.providers.mistral_provider import MistralProvider
from llx.providers.gemini_provider import GeminiProvider
from llx.providers.perplexity_provider import PerplexityProvider
from llx.providers.provider import Provider
import asyncio
from typing import Any, AsyncIterator

from llx.providers.xai_provider import XAIProvider


def get_provider(provider: str, model: str) -> Provider:
    if provider == 'openai':
        return OpenAIProvider(model)
    elif provider == 'ollama':
        return OllamaProvider(model)
    elif provider == 'anthropic':
        return AnthropicProvider(model)
    elif provider == 'deepseek':
        return DeepseekProvider(model)
    elif provider == 'mistral':
        return MistralProvider(model)
    elif provider == 'gemini':
        return GeminiProvider(model)
    elif provider == 'xai':
        return XAIProvider(model)
    elif provider == 'perplexity':
        return PerplexityProvider(model)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

async def fetch_api_response(provider: str, model: str, prompt: str, attachment: str=None) -> AsyncIterator[str]:
    """
    Calls the appropriate API based on the provider and returns the response.

    Parameters:
        provider (str): The LLM provider, ex ollama or openai.
        prompt (str): The user input to send to the model.
        model (str): The model to use.
    
    Returns:
        AsyncIterator[str]: The response from the API.
    """
    if provider == 'openai':
        api_provider = OpenAIProvider(model, prompt, attachment)
    elif provider == 'ollama':
        api_provider = OllamaProvider(model, prompt)
    elif provider == 'anthropic':
        api_provider = AnthropicProvider(model, prompt, attachment)
    elif provider == 'deepseek':
        api_provider = DeepseekProvider(model, prompt, attachment)
    elif provider == 'mistral':
        api_provider = MistralProvider(model, prompt, attachment)
    elif provider == 'gemini':
        api_provider = GeminiProvider(model, prompt, attachment)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    async for response in api_provider.invoke():
        yield response

