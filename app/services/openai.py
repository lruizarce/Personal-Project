from openai import AsyncOpenAI
import openai
from app.utils.exceptions import LLMServiceError
import os
from dotenv import load_dotenv
load_dotenv()
import time
from app.schemas.chat import ChatRequest, UsageInfo, ChatResponse


async def openai_response(request: ChatRequest) -> ChatResponse:
    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model = request.model or os.environ.get("OPENAI_DEFAULT_MODEL")
    max_tokens = request.max_tokens or int(os.environ.get("OPENAI_DEFAULT_MAX_TOKENS"))
    temperature = request.temperature or float(os.environ.get("OPENAI_DEFAULT_TEMPERATURE", 0.7))
    
    start_time = time.perf_counter()
    try:
        response = await client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=request.messages  
        )
    except openai.AuthenticationError as e:
        raise LLMServiceError(
            message="LLM service configuration error",
            status_code=500,
            original_error=e
        )
    except openai.RateLimitError as e:
        raise LLMServiceError(
            message="Rate limit exceeded. Please try again later.",
            status_code=429,
            original_error=e
        )
    except openai.APIConnectionError as e:
        raise LLMServiceError(
            message="Unable to connect to LLM service",
            status_code=502,
            original_error=e
        )
    except openai.BadRequestError as e:
        raise LLMServiceError(
            message=f"Invalid request: {str(e)}",
            status_code=400,
            original_error=e
        )
    except openai.APIStatusError as e:
        raise LLMServiceError(
            message="LLM service error",
            status_code=502,
            original_error=e
        )

    end_time = time.perf_counter()
    latency_ms = int((end_time - start_time) * 1000)
    
    return ChatResponse(
        id=response.id,
        content=response.choices[0].message.content,
        model=response.model,
        usage=UsageInfo(
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens
        ),
        latency_ms=latency_ms
    )