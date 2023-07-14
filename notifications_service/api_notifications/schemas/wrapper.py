from jinja2 import Template, TemplateSyntaxError
from pydantic import BaseModel, validator


class AddWrapperDB(BaseModel):
    id_event: int
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


class WrapperDB(AddWrapperDB):
    id_wrapper: int


class EditWrapperDB(AddWrapperDB):
    id_wrapper: int


class DeleteWrapperDB(BaseModel):
    id_wrapper: int
