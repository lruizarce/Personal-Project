from datetime import datetime as dt, timezone
from uuid import UUID

from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from ..database import SessionDep
from ..models.conversations import Conversation
from ..models.message import Message

router = APIRouter(prefix='/conversations')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_conversation(session: SessionDep, conversation: Conversation) -> Conversation:
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


@router.get("/", status_code=status.HTTP_200_OK)
async def get_conversations(session: SessionDep) -> list[Conversation]:
    result = await session.execute(select(Conversation).where(Conversation.deleted_at == None))
    return result.scalars().all()

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_conversation_details(id: UUID, session: SessionDep) -> Conversation:
    result = await session.execute(select(Conversation).where(Conversation.id == id, Conversation.deleted_at == None))
    conversation = result.scalars().first()

    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")
    return conversation

@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_conversation(id: UUID, session: SessionDep, updates: dict) -> Conversation:
    result = await session.execute(select(Conversation).where(Conversation.id == id, Conversation.deleted_at == None))
    conversation = result.scalars().first()

    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")
    for k, v in updates.items():
        if hasattr(conversation, k):
            setattr(conversation, k, v)

    await session.commit()
    return conversation

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(id: UUID, session: SessionDep):
    result = await session.execute(select(Conversation).where(Conversation.id == id, Conversation.deleted_at == None))
    conversation = result.scalars().first()

    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")

    conversation.deleted_at = dt.now(timezone.utc)
    await session.commit()

@router.get("/{id}/messages", status_code=status.HTTP_200_OK)
async def get_messages_conversation(id: UUID, session: SessionDep) -> list[Message]:
    result = await session.execute(select(Message).where(Message.conversation_id == id, Message.deleted_at == None))
    messages = result.scalars().all()

    if not messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No messages found")

    return messages

@router.delete("/{id}/messages", status_code=status.HTTP_204_NO_CONTENT)
async def delete_messages(id: UUID, session: SessionDep):
    result = await session.execute(select(Message).where(Message.conversation_id == id, Message.deleted_at == None))
    messages = result.scalars().all()

    if not messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No messages found")

    for message in messages:
        message.deleted_at = dt.now(timezone.utc)
    await session.commit()