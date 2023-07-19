from pydantic import BaseModel


class UnsubscribeDB(BaseModel):
    id_unsubscriber: int
    id_event: int
    id_user: str


class EditUnsubscribeDB(UnsubscribeDB):
    pass


class AddUnsubscribeDB(BaseModel):
    id_event: int
    id_user: str


class RemoveUnsubscribeDB(BaseModel):
    id_unsubscriber: int
