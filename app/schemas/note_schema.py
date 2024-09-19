from pydantic import BaseModel, Field
from typing import Annotated


class NotesBase(BaseModel):
    title: Annotated[str, Field(max_length=50)]
    text: Annotated[str, Field(max_length=500)]

    class Config:
        from_attributes = True


class NotesSchema(NotesBase):
    id: Annotated[int, Field(gt=0)]
    user_id: Annotated[int, Field(gt=0)]
