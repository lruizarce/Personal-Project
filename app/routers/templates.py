from datetime import datetime as dt, timezone
from uuid import UUID

from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from ..database import SessionDep
from ..models.promptTemplate import PromptTemplate
from ..schemas.template import RenderRequest, RenderResponse

from typing import List

router = APIRouter(prefix="/templates")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_template(session:SessionDep, template:PromptTemplate)->PromptTemplate:
    session.add(template)
    await session.commit()
    await session.refresh(template)
    return template


@router.get("", status_code=status.HTTP_200_OK)
async def get_templates(session:SessionDep) -> List[PromptTemplate]:
    result = await session.execute(select(PromptTemplate).where(PromptTemplate.deleted_at == None))
    return result.scalars().all()


@router.get("{id}", status_code=status.HTTP_200_OK)
async def get_templates_by_id(id:int, session:SessionDep) -> PromptTemplate:
    result = await session.execute(select(PromptTemplate).where(PromptTemplate.id == id))
    template = result.scalars().first()
    
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
    
    return template
    

@router.get("/name/{name}", status_code=status.HTTP_200_OK)
async def get_templates_by_name(name: str, session:SessionDep) -> PromptTemplate:
    result = await session.execute(select(PromptTemplate).where(PromptTemplate.name == name))
    templateName = result.scalars().first()

    if not templateName:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template {name} not found.")
    
    return templateName


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_template(id:UUID, session:SessionDep, updates:dict) -> PromptTemplate:
    result = await session.execute(select(PromptTemplate.id).where(PromptTemplate.id == id))
    template = result.scalars().first()

    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template {id} not found.")
    
    for k,v in updates.model_dump(exclude_unset=True).items():
        setattr(template, k, v)
    
    template.updated_at = dt.now(timezone.utc)
    await session.commit()
    await session.refresh(template)
    return template


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_template(id:UUID, session:SessionDep) -> PromptTemplate:
    result = session.execute(select(PromptTemplate).where(PromptTemplate.id == id))
    template = result.scalars().first()

    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template {id} not found.")
    
    template.deleted_at = dt.now(timezone.utc)
    await session.commit()


@router.post("/{id}/render", status_code=status.HTTP_200_OK)
async def render_template(id: UUID, session: SessionDep, request: RenderRequest) -> RenderResponse:
    result = await session.execute(select(PromptTemplate).where(PromptTemplate.id == id, PromptTemplate.deleted_at == None))
    template = result.scalars().first()

    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Template {id} not found.")

    rendered_content = template.content


    missing_vars = []
    for var in template.variables:
        if var.required and var.name not in request.variables:
            missing_vars.append(var.name)

    if missing_vars:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required variables: {', '.join(missing_vars)}"
        )

    for var_name, var_value in request.variables.items():
        rendered_content = rendered_content.replace(f"{{{{{var_name}}}}}", var_value)

    return RenderResponse(
        template_id=template.id,
        template_name=template.name,
        rendered_content=rendered_content
    )

