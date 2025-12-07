from typing import Literal, List, Annotated
from pydantic import BaseModel, Field



class MessageInput(BaseModel):
    role: Literal["system","user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: Annotated[list[MessageInput], Field(min_length=1)]
    model: str | None = None
    max_tokens: Annotated[int | None, Field(gt=0)] = None
    temperature: Annotated[float | None, Field(ge=0.0, le=1.0)] = None
    system_prompt: str | None = None

class UsageInfo(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int

class ChatResponse(BaseModel):
    id: str
    content: str
    model: str
    usage: UsageInfo
    latency_ms: int