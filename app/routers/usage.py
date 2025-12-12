
from fastapi import APIRouter, HTTPException, status
from ..database import SessionDep

from typing import List

from ..models.usageLog import UsageLog
from uuid import UUID

from typing import Optional
from datetime import datetime as dt, timezone
from sqlmodel import select

router = APIRouter(prefix="/usage")

@router.get("/summary", status_code=status.HTTP_200_OK)
async def get_summary(session: SessionDep, date: Optional[dt] = None) -> List[UsageLog]:

    if not date:
        result = session.execute(select(UsageLog))
        summary = result.scalars().all()
    else:
        result = session.execute(select(UsageLog).where(UsageLog.created_at == date))
        summary = result.scalars().all()

    
    if not summary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data")
    
    return summary


@router.get("/by-model", status_code=status.HTTP_200_OK)
async def get_stats_by_model(session: SessionDep, model: str) -> List[UsageLog]:
    result = session.execute(select(UsageLog).where(UsageLog.model == model))
    summary = result.scalars().all()

    if not summary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data")
    
    return summary

@router.get("/by-conversation/{id}", status_code=status.HTTP_200_OK)
async def get_conversation_by_id(id: UUID, session: SessionDep) -> List[UsageLog]:
    result = session.execute(select(UsageLog).where(UsageLog.conversation_id == id))
    logs = result.scalars().all()

    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No usage logs found for this conversation")

    return logs


@router.get("/logs", status_code=status.HTTP_200_OK)
async def get_logs(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[str] = None,
    model: Optional[str] = None
) -> List[UsageLog]:
    query = select(UsageLog)

    if user_id:
        query = query.where(UsageLog.user_id == user_id)
    if model:
        query = query.where(UsageLog.model == model)

    query = query.offset(skip).limit(limit)
    result = session.execute(query)
    return result.scalars().all()
