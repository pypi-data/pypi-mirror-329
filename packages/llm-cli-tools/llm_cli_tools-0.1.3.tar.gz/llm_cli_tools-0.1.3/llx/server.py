import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from fastapi.responses import StreamingResponse
import asyncio
from llx.utils import fetch_api_response, get_provider  # Import the fetch_api_response function
import json
import logging

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]

class Choice(BaseModel):
    index: int
    message: Message
    logprobs: Any = None
    finish_reason: str

class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages are required")

    provider, model = request.model.split(':', 1)
    client = get_provider(provider, model)
    prompt = "\n".join([f"role: {message.role}\nmessage: {message.content}" for message in request.messages])
    
    print(f"Provider: {provider}, Model: {model}, Prompt: {prompt}")
    try:
        async def response_generator():
            response = {
                "id": "chatcmpl-123",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": request.model,
                "choices": [],
                "usage": {
                    "completion_tokens": 0,
                    "total_tokens": 0
                }
            }
            try:
                async for chunk in client.invoke(prompt):
                    print(chunk)
                    response["choices"].append({
                        "index": len(response["choices"]),
                        "message": {
                            "role": "assistant",
                            "content": chunk,
                        },
                        "logprobs": None,
                        "finish_reason": "stop"
                    })
                    response["usage"]["completion_tokens"] += len(chunk.split())
                    response["usage"]["total_tokens"] += len(chunk.split())
                    yield json.dumps(response)
            except Exception as e:
                raise HTTPException(status_code=500, detail="Internal Server Error")

        return StreamingResponse(response_generator(), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
