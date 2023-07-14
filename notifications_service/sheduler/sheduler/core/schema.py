from typing import Any, Callable, Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Optional[Callable[[Any], Any]]) -> str:
    return orjson.dumps(v, default=default).decode()


class ConfigMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class LikesModel(ConfigMixin):
    user_id: int
    count: int
    comment_id: int


class CommentModel(ConfigMixin):
    user_id: int
    text: int
    comment_id: int
    parent_comment_id: int


class NewsModel(ConfigMixin):
    name: int
    film_id: int
    poster: str
    link: str
