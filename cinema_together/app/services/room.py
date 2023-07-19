
import logging
from functools import lru_cache
from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from models.postgres import Room, RoomUser
from models.scheme import RoomUserType, CustomUser
from services.utils import get_random_string

logger = logging.getLogger(__name__)


class RoomService:
    def __init__(self, db_connection: AsyncEngine):
        self.db_connection = db_connection

    def get_session(self) -> AsyncSession:
        return sessionmaker(self.db_connection, expire_on_commit=False,
                            class_=AsyncSession)()

    async def create_room(
            self, room_id: UUID, user_id: str, link: str, film_id: UUID, members: list[UUID]
    ):
        async with self.get_session() as session:
            try:
                async with session.begin():
                    room = Room(
                        id=room_id,
                        creator_id=user_id,
                        film_id=film_id,
                        room_link=link
                    )
                    room_user = RoomUser(user_id=user_id, temp_token=get_random_string(16),
                                         user_type=RoomUserType.creator.value)
                    room.room_users.append(room_user)
                    for member in members:
                        room.room_users.append(
                            RoomUser(
                                user_id=member,
                                temp_token=get_random_string(16),
                                user_type=RoomUserType.viewer.value
                            )
                        )
                    session.add(room)
                    await session.commit()
            except IntegrityError as e:
                logger.error(e)
                return 'Комната уже существует!'

    async def connect(self, user: CustomUser, room_id: str) -> Optional[str]:
        async with self.db_connection.begin() as conn:
            room_user = await conn.execute(
                select(RoomUser).where(RoomUser.room_id == room_id).where(RoomUser.user_id == user.id))
            room_user = room_user.scalars().first()
            if not room_user:
                return f'Вы не имеете доступа к комнате!'

    async def check_token(self, room_id, user_id, token):
         async with self.db_connection.begin() as conn:
            room_user = await conn.execute(
                select(RoomUser).where(RoomUser.room_id == room_id).where(RoomUser.user_id == user_id))
            room_user = room_user.scalars().first()
            if room_user.temp_token == token:
                return True

    async def disconnect_user(self, user: CustomUser, room_id: str):
        async with self.db_connection.begin_async() as conn:
            result = await conn.execute(
                delete(RoomUser)
                .where(RoomUser.room_id == str(room_id))
                .where(RoomUser.user_id == str(user.id))
                .execution_options(synchronize_session=False)
            )
            if result.rowcount > 0:
                return True
            return f'Ошибка! Юзер "{user.id}" в комнате отсутствует!'


async_pg_engine: Optional[AsyncEngine] = create_async_engine(settings.pg_dsn)


async def get_pg_engine() -> Optional[async_pg_engine]:
    return async_pg_engine


@lru_cache()
def get_room_service(
        db_connection: AsyncEngine = Depends(get_pg_engine),
) -> RoomService:
    return RoomService(db_connection)
