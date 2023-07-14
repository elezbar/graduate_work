from datetime import datetime
from pydantic import BaseModel


class AddSendedNotification(BaseModel):
    id_user: int
    type_notification: str
    message: str
    date_send: datetime
    date_check: datetime | None


class SendedNotificationDB(AddSendedNotification):
    id_sended_notification: int


class DeleteSendedNotification(BaseModel):
    id_sended_notification: int


class CheckSendedNotification(BaseModel):
    id_sended_notification: int
