from datetime import datetime
from pydantic import BaseModel


class AddNotificationDB(BaseModel):
    id_event: int
    id_user: str | None
    last_update: datetime | None
    last_notification_send: datetime | None


class NotificationDB(AddNotificationDB):
    id_notification: int


class EditNotificationDB(AddNotificationDB):
    id_notification: int


class UpdateDataNotificationDB(BaseModel):
    id_content: int


class DeleteNotificationDB(BaseModel):
    id_notification: int
