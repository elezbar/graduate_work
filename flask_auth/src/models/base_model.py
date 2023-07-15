import uuid
from typing import Any

from sqlalchemy import MetaData, inspect
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from utils.utils import camelcase_to_snake

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


@as_declarative(metadata=meta)
class BaseModel:
    __allow_unmapped__ = True

    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:  # noqa
        return camelcase_to_snake(cls.__name__)

    def serialize(self) -> dict:
        result_dict = {}
        serialize_types = {uuid.UUID: str}
        insp = inspect(self)
        if insp:
            for c in insp.mapper.column_attrs:
                value = getattr(self, c.key)
                if len(c.key) > 0 and c.key[0] == "_":
                    continue
                if type(value) in serialize_types:
                    result_dict[c.key] = serialize_types[type(value)](value)
                else:
                    result_dict[c.key] = value
        return result_dict
