import logging
from functools import lru_cache
from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models.postgres import Room, RoomUser
from models.scheme import RoomUserType, CustomUser

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
                        room_link=link,
                        members=members
                    )
                    room_user = RoomUser(user_id=user_id,
                                         user_type=RoomUserType.creator.value)
                    room.room_users.append(room_user)
                    session.add(room)
                    await session.commit()
            except IntegrityError as e:
                logger.error(e)
                return 'Комната уже существует!'

    async def connect(self, user: CustomUser, room_id: str) -> Optional[str]:
        async with self.db_connection.begin() as conn:
            room = await conn.execute(
                select(Room.creator_id).where(Room.id == room_id))
            room_creator = room.scalars().first()
            if not room_creator:
                return f'Комната "{room_id}" не существует!'
            if user.id == room_creator:
                return f'Вы и так создатель комнаты "{room_id}"!'
            try:
                await conn.execute(
                    insert(RoomUser).values(
                        room_id=room_id,
                        user_id=user.id,
                        user_type=RoomUserType.viewer.value
                    )
                )
            except IntegrityError as exc:
                logger.error(exc)
                return f'Room user "{user.id}" already exists!'

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


async_pg_engine: Optional[AsyncEngine] = None


async def get_pg_engine() -> Optional[async_pg_engine]:
    return async_pg_engine


@lru_cache()
def get_room_service(
        db_connection: AsyncEngine = Depends(get_pg_engine),
) -> RoomService:
    return RoomService(db_connection)
