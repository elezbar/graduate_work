from models.models import Role, User, UserRole


def test_delete_user_role(client, session, access):
    url = "/api/v1/user_role/{id}"
    name_user = "TestUser"
    name_role = "TestRole"
    user = User(username=name_user, _password="123")
    session.add(user)
    role = Role(name=name_role)
    session.add(role)
    session.commit()
    user_role = UserRole(
        user_id=str(user.id),
        role_id=str(role.id),
    )
    session.add(user_role)
    session.commit()
    id_user_role = str(user_role.id)
    client.delete(url.format(id=str(user_role.id)), headers={"Authorization": access})
    deleted_user_role = session.query(UserRole).filter_by(id=id_user_role).all()
    assert len(deleted_user_role) == 0
    if len(deleted_user_role) != 0:
        session.delete(user_role)
        session.commit()
    session.delete(role)
    session.delete(user)
    session.commit()
