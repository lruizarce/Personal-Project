from uuid import UUID, uuid4
from datetime import datetime as dt, timezone
from typing import List
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column, JSON


class VariableDefinition(BaseModel):
    name: str
    description: str
    required: bool = True


class PromptTemplate(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Auto generated unique identifier")
    name: str = Field(description="Unique identifier for template")
    description: str | None = Field(default=None, description="Optional description")
    content: str = Field(description="Template with {{variable}} placeholders")
    variables: List[VariableDefinition] = Field(default=[], sa_column=Column(JSON))
    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc), description="Timestamp when template was created")
    updated_at: dt = Field(default_factory=lambda: dt.now(timezone.utc), description="Timestamp when template was last updated")
    deleted_at: dt | None = Field(default=None, description="Timestamp when template was soft deleted")