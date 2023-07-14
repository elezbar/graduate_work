from typing import Any
from jinja2 import Template, TemplateSyntaxError
from pydantic import BaseModel, validator


class InstantNotification(BaseModel):
    id_user: list[int]
    template: str
    type_notification: str

    @validator('template')
    def valid_template(cls, v, values):
        try:
            tm = Template(v)
            tm.render()
        except TemplateSyntaxError:
            raise ValueError('template is not rendered correctly')
        return v


class UserNotificationData(BaseModel):
    id_user: int
    data: dict[str, Any]


class DelayedNotification(BaseModel):
    user_data: list[UserNotificationData]
    template: str
    type_notification: str

    @validator('template')
    def valid_template(cls, v, values):
        try:
            tm = Template(v)
            tm.render()
        except TemplateSyntaxError:
            raise ValueError('template is not rendered correctly')
        return v
