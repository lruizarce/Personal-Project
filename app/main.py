from fastapi import FastAPI

from app.routers.chat import router


app = FastAPI(title="LLM Service", description="Test descripton", version='1.0.0')
app.include_router(router)


@app.get("/health")
async def index():
    return {"status":"ok!"}

