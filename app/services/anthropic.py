from app.schemas.chat import ChatRequest, UsageInfo, ChatResponse
from app.utils.exceptions import LLMServiceError
import os
from dotenv import load_dotenv
import time
import anthropic

load_dotenv()

async def anthropic_response(request: ChatRequest) -> ChatResponse:
    client = anthropic.AsyncAnthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    messages = [
        {"role": msg.role, "content": msg.content}
        for msg in request.messages
        if msg.role != "system"
    ]
    
    model = request.model or os.environ.get("DEFAULT_MODEL")
    max_tokens = request.max_tokens or int(os.environ.get("DEFAULT_TOKENS", 4096))
    
    start_time = time.perf_counter()
    
    try:
        response = await client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=request.temperature or 0.7,
            system=request.system_prompt or "",
            messages=messages
        )
    except anthropic.AuthenticationError as e:
        raise LLMServiceError(
            message="LLM service configuration error",
            status_code=500,
            original_error=e
        )
    except anthropic.RateLimitError as e:
        raise LLMServiceError(
            message="Rate limit exceeded. Please try again later.",
            status_code=429,
            original_error=e
        )
    except anthropic.APIConnectionError as e:
        raise LLMServiceError(
            message="Unable to connect to LLM service",
            status_code=502,
            original_error=e
        )
    except anthropic.BadRequestError as e:
        raise LLMServiceError(
            message=f"Invalid request: {str(e)}",
            status_code=400,
            original_error=e
        )
    except anthropic.APIStatusError as e:
        raise LLMServiceError(
            message="LLM service error",
            status_code=502,
            original_error=e
        )
    
    end_time = time.perf_counter()
    latency_ms = int((end_time - start_time) * 1000)
    
    return ChatResponse(
        id=response.id,
        content=response.content[0].text,
        model=response.model,
        usage=UsageInfo(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.input_tokens + response.usage.output_tokens
        ),
        latency_ms=latency_ms
    )