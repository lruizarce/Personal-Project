from fastapi import FastAPI

from app.routers.chat import router as chat_router
from app.routers.conversations import router as conversations_router
from app.routers.templates import router as templates_router
from app.routers.models import router as models_router
from app.routers.usage import router as usage_router


app = FastAPI(title="LLM Service", description="Test descripton", version='1.0.0')
app.include_router(chat_router)
app.include_router(conversations_router)
app.include_router(templates_router)
app.include_router(models_router)
app.include_router(usage_router)


@app.get("/health")
async def index():
    return {"status":"ok!"}

