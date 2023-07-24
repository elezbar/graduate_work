import uuid

from sqlalchemy import (
    Column, String, DateTime, func, UUID, Boolean, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Room(Base):
    __tablename__ = 'movie_together_room'
    __table_args__ = (
        {'schema': 'cinema'}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False)
    creator_id = Column(UUID, nullable=False, unique=True)
    film_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime, server_default=func.now())
    active = Column(Boolean, default=True)
    room_link = Column(String(255))
    room_users = relationship('RoomUser')

    __mapper_args__ = {'eager_defaults': True}


class RoomUser(Base):
    __tablename__ = 'movie_together_room_users'
    __table_args__ = (
        UniqueConstraint('user_id', 'room_id', name='unique_room_user'),
        {'schema': 'cinema'},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False)
    room_id = Column(ForeignKey(Room.id, ondelete='CASCADE'))
    user_id = Column(UUID(as_uuid=True))
    user_type = Column(String(255))  # создатель комнаты или простой зритель
    temp_token = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
