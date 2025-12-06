from typing import Literal, List
from pydantic import BaseModel, Field



class MessageInput(BaseModel):
    role: Literal["system","user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[MessageInput] = Field(min_length=1)
    model: str | None = None
    max_tokens: int | None = Field(default=None, gt=0)
    temperature: float | None = Field(default=None, ge=0.0, le=1.0)
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