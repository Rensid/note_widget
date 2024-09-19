from app.integration.speller import validate_errors
from app.models.user_model import User
from app.models.note_model import Notes
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.note_schema import NotesBase


async def create_note(session: AsyncSession, user: User, note_data: NotesBase):
    await validate_errors(note_data.text)
    new_note = Notes(title=note_data.title,
                     text=note_data.text, owner_id=user.id)
    session.add(new_note)
    await session.commit()
    return new_note


async def get_all_user_notes(session: AsyncSession, user: User):
    notes = await session.execute(select(Notes).where(Notes.owner_id == user.id))
    return notes.scalars().all()


async def select_notes_by_title(session: AsyncSession, user: User, title: str):
    notes = await session.execute(select(Notes).where(Notes.title == title, Notes.owner_id == user.id))
    return notes.scalars().all()
