from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.auth.auth import get_current_user
from app.db.base import get_async_session
from app.models.user_model import User
from app.schemas.note_schema import NotesBase, NotesSchema
from app.crud.note_crud import create_note, get_all_user_notes, select_notes_by_title

note_router = APIRouter()


@note_router.post('/notes/create')
async def create_new_note(note_data: NotesBase, user: User = Depends(get_current_user),
                          session: Session = Depends(get_async_session)):
    note = await create_note(session, user, note_data)
    return note


@note_router.get('/notes/get_all', response_model=List[NotesBase])
async def get_all_notes(session: Session = Depends(get_async_session),
                        user: User = Depends(get_current_user)):
    notes = await get_all_user_notes(session, user)
    return [NotesBase.from_orm(note) for note in notes]


@note_router.get('/notes/title/{title}', response_model=List[NotesBase])
async def get_note_by_title(title: str,
                            session: Session = Depends(get_async_session),
                            user: User = Depends(get_current_user)):
    notes = await select_notes_by_title(session, user, title)
    return [NotesBase.from_orm(note) for note in notes]
