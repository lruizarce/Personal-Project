
from fastapi import APIRouter, status, HTTPException

from app.models.usageLog import UsageLog

from typing import List

from ..database import SessionDep

from sqlmodel import select




router = APIRouter(prefix='/models')

@router.get("", status_code=status.HTTP_200_OK)
async def get_models(session:SessionDep )->List[UsageLog]:
    result = session.execute(select(UsageLog.model))
    return result.scalars().all()

@router.get("/{model_id}", status_code=status.HTTP_200_OK)
async def get_model_by_id(model_id:str, session:SessionDep)->UsageLog:
    result = session.execute(select(UsageLog).where(UsageLog.model ==model_id))
    model = result.scalars().first()

    if not model:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail ="Model not found" )
    
    return model