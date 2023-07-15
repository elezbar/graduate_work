from uuid import uuid4

from flask import Blueprint

import models
from db.alchemy import session
from utils.passwords.service import PasswordManager

utils_bp = Blueprint("utils_bp", __name__, url_prefix="/utils_bp")


@utils_bp.cli.command("init_db")
@session
def create_db_initial_data(session):
    """flask utils_bp init_db"""
    role1 = models.Role(id="eaa259ca-1b78-41f8-a345-38411a65803b", name="anonimous")
    role2 = models.Role(id="78879608-0148-4f3e-9e16-356994d989d2", name="regular")
    role3 = models.Role(id="4cbf2021-8505-420a-af6f-1bf8bb1689aa", name="subscriber")
    role4 = models.Role(id="f70a78f6-fb93-4a47-b8eb-e325211ad4e9", name="manager")
    role5 = models.Role(id="f8f5ee59-af86-4fd3-a11f-75d233dbd7fa", name="superuser")

    password = PasswordManager.generate_hash(password="qwerty100500")
    user1 = models.User(id="e5fcf716-4121-4b64-b23b-b6d63a14a850", username="username1", _password=password)
    user2 = models.User(id="e5fcf716-4121-4b64-b23b-b6d63a14a851", username="username2", _password=password)
    user3 = models.User(id="e5fcf716-4121-4b64-b23b-b6d63a14a852", username="username3", _password=password)
    user4 = models.User(id="e5fcf716-4121-4b64-b23b-b6d63a14a853", username="username4", _password=password)

    user_role1 = models.UserRole(user_id=user1.id, role_id=role5.id)
    user_role2 = models.UserRole(user_id=user2.id, role_id=role2.id)
    user_role3 = models.UserRole(user_id=user2.id, role_id=role3.id)
    user_role4 = models.UserRole(user_id=user3.id, role_id=role4.id)
    user_role5 = models.UserRole(user_id=user4.id, role_id=role2.id)
    user_role6 = models.UserRole(user_id=user4.id, role_id=role3.id)

    permission_object_movie = models.PermissionObject(id=uuid4(), name="movie")
    permission_object_genre = models.PermissionObject(id=uuid4(), name="genre")
    permission_object_person = models.PermissionObject(id=uuid4(), name="person")
    permission_object_user = models.PermissionObject(id=uuid4(), name="user")
    permission_object_permission = models.PermissionObject(id=uuid4(), name="permission")
    permission_object_role = models.PermissionObject(id=uuid4(), name="role")
    permission_object_category_subscribers = models.PermissionObject(id=uuid4(), name="subscribers")

    permission1 = models.Permission(
        id=uuid4(),
        permission_object_id=permission_object_movie.id,
        role_id=role3.id,
        permitted_action="read",
        object_id=None,
    )
    permission2 = models.Permission(
        id=uuid4(),
        permission_object_id=permission_object_person.id,
        role_id=role1.id,
        permitted_action="read",
        object_id=None,
    )
    permission3 = models.Permission(
        id=uuid4(),
        permission_object_id=permission_object_person.id,
        role_id=role2.id,
        permitted_action="read",
        object_id=None,
    )
    permission4 = models.Permission(
        id=uuid4(),
        permission_object_id=permission_object_category_subscribers.id,
        role_id=role4.id,
        permitted_action="read",
        object_id=None,
    )
    permission5 = models.Permission(
        id=uuid4(),
        permission_object_id=permission_object_movie.id,
        role_id=role4.id,
        permitted_action="read",
        object_id=None,
    )
    permission6 = models.Permission(
        id=uuid4(),
        permission_object_id=permission_object_movie.id,
        role_id=role4.id,
        permitted_action="create",
        object_id=None,
    )
    permission7 = models.Permission(
        id=uuid4(),
        permission_object_id=permission_object_user.id,
        role_id=role1.id,
        permitted_action="create",
        object_id=None,
    )
    permission8 = models.Permission(
        id=uuid4(),
        permission_object_id=permission_object_user.id,
        role_id=role5.id,
        permitted_action="create",
        object_id=None,
    )
    permission9 = models.Permission(
        id=uuid4(),
        permission_object_id=permission_object_category_subscribers.id,
        role_id=role3.id,
        permitted_action="read",
        object_id=None,
    )

    roles = [
        role1,
        role2,
        role3,
        role4,
        role5,
    ]
    users = [user1, user2, user3, user4]
    user_roles = [user_role1, user_role2, user_role3, user_role4, user_role5, user_role6]
    permission_objects = [
        permission_object_movie,
        permission_object_category_subscribers,
        permission_object_person,
        permission_object_user,
        permission_object_genre,
        permission_object_role,
        permission_object_permission,
    ]
    permissions = [
        permission1,
        permission2,
        permission3,
        permission4,
        permission5,
        permission6,
        permission7,
        permission8,
        permission9,
    ]
    session.bulk_save_objects(permission_objects)
    session.commit()
    session.bulk_save_objects(roles)
    session.commit()
    session.bulk_save_objects(users)
    session.commit()
    session.bulk_save_objects(user_roles)
    session.commit()
    session.bulk_save_objects(permissions)
    session.commit()
