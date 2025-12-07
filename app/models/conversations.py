from typing import Annotated
from uuid import UUID, uuid4

from fastapi import FastAPI, Form
from pydantic import BaseModel, Field

from datetime import datetime as dt


class Conversations(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: str
    title:str
    model:str
    system_prompt:str
    created_at:str
    update_at:str
