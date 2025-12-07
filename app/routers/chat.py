from fastapi import FastAPI, APIRouter, status, HTTPException
from ..schemas.chat import ChatRequest, ChatResponse
from ..services.anthropic import anthropic_response as llm
from ..utils.exceptions import LLMServiceError

app = FastAPI()
router = APIRouter(prefix='/chat')

@router.post("/completions", status_code=status.HTTP_200_OK)
async def chats(request: ChatRequest) -> ChatResponse:
    try:
        llm_service = await llm(request)
        return llm_service
    except LLMServiceError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

app.include_router(router)