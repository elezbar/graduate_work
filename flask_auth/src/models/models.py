from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID

from models.base_model import BaseModel


class User(BaseModel):
    # __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(255))
    _password = Column('password', String(255), nullable=False)

    def __str__(self) -> str:
        return f'<User {self.username}>'

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, hashed_password):
        self._password = hashed_password


class UserRole(BaseModel):
    # __tablename__ = 'user_role'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'))
    role_id = Column('role_id', UUID(as_uuid=True), ForeignKey('role.id'))


class Role(BaseModel):
    # __tablename__ = 'role'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    name = Column(String(80), unique=True, nullable=False)


class AuthHistory(BaseModel):
    # __tablename__ = 'history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    device = Column(Text, nullable=False)
    datetime = Column(DateTime, server_default=func.now())
    endpoint = Column(String(128), nullable=False)
    action = Column(String(24), nullable=False)


class Permission(BaseModel):
    # __tablename__ = 'permission'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    permission_object_id = Column('permission_object_id', UUID(as_uuid=True), ForeignKey('permission_object.id'))
    role_id = Column('role_id', UUID(as_uuid=True), ForeignKey('role.id'))
    permitted_action = Column(String(24))
    object_id = Column('object_id', UUID(as_uuid=True), nullable=True)


class PermissionObject(BaseModel):
    # __tablename__ = 'permission_object'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    name = Column(String(80), unique=True, nullable=False)
