from typing import Literal, Annotated
from pydantic import BaseModel, Field


class MessageInput(BaseModel):
    role: Annotated[Literal["system", "user", "assistant"], Field(description="Role of the message sender")]
    content: Annotated[str, Field(description="Content of the message")]

class ChatRequest(BaseModel):
    messages: Annotated[list[MessageInput], Field(min_length=1, description="List of messages in the conversation")]
    model: Annotated[str | None, Field(description="Model to use for completion")] = None
    max_tokens: Annotated[int | None, Field(gt=0, description="Maximum tokens in response")] = None
    temperature: Annotated[float | None, Field(ge=0.0, le=1.0, description="Sampling temperature")] = None
    system_prompt: Annotated[str | None, Field(description="Optional system prompt override")] = None

class UsageInfo(BaseModel):
    input_tokens: Annotated[int, Field(description="Number of tokens in the input")]
    output_tokens: Annotated[int, Field(description="Number of tokens in the output")]
    total_tokens: Annotated[int, Field(description="Total tokens used")]

class ChatResponse(BaseModel):
    id: Annotated[str, Field(description="Unique identifier for the response")]
    content: Annotated[str, Field(description="Generated response content")]
    model: Annotated[str, Field(description="Model used for generation")]
    usage: Annotated[UsageInfo, Field(description="Token usage information")]
    latency_ms: Annotated[int, Field(description="Response latency in milliseconds")]