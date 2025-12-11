from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class RenderRequest(BaseModel):
    variables: Annotated[dict[str, str], Field(default={}, description="Dictionary of variable names to values for substitution")]


class RenderResponse(BaseModel):
    template_id: Annotated[UUID, Field(description="ID of the rendered template")]
    template_name: Annotated[str, Field(description="Name of the rendered template")]
    rendered_content: Annotated[str, Field(description="Template content with variables substituted")]
