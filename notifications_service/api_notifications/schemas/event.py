from datetime import datetime
from pydantic import BaseModel


class AddEventDB(BaseModel):
    name: str
    last_call: datetime | None
    interval: datetime | None


class EventDB(AddEventDB):
    id_event: int


class EditEventDB(AddEventDB):
    id_event: int


class DeleteEventDB(BaseModel):
    id_event: int
