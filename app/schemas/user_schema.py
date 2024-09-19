from pydantic import BaseModel, Field
from typing import Annotated, Union
from app.schemas.note_schema import NotesSchema


class UserBase(BaseModel):
    username: Annotated[str, Field(max_length=50)]

    class Config:
        from_attributes = True


class UserPasswordSchema(UserBase):
    hashed_password: str


class UserSchema(UserBase):
    id: Annotated[int, Field(gt=0)]


class TokenData(BaseModel):
    id: Union[int, None] = None
    username: Union[str, None] = None


class Token(BaseModel):
    access: str
    refresh: str
