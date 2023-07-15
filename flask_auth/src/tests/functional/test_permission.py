from uuid import uuid4

import pytest

from models.models import Permission, PermissionObject, Role


@pytest.fixture()
def params(session):
    url = "/api/v1/permission/{id}"
    name_perm_obj = "TestPermissionObject"
    name_role = "TestRole"
    obj_id = str(uuid4())
    perm_obj = PermissionObject(name=name_perm_obj)
    session.add(perm_obj)
    session.commit()
    role = Role(name=name_role)
    session.add(role)
    session.commit()
    perm = Permission(
        permission_object_id=str(perm_obj.id), role_id=str(role.id), permitted_action="get", object_id=obj_id
    )
    session.add(perm)
    session.commit()
    return {'url': url, 'role': role, 'perm': perm, 'perm_obj': perm_obj, 'obj_id': obj_id}


def test_get_permission(client, session, access, params):
    response = client.get(params['url'].format(id=str(params['perm'].id)), headers={"Authorization": access})
    response_json = response.json
    session.delete(params['role'])
    session.delete(params['perm_obj'])
    session.delete(params['perm'])
    session.commit()
    assert response_json.get("role_id") == str(params['role'].id)
    assert response_json.get("permitted_action") == "get"
    assert response_json.get("object_id") == params['obj_id']
    assert response_json.get("permission_object_id") == str(params['perm_obj'].id)


def test_delete_permission(client, session, access, params):
    id_perm = str(params['perm'].id)
    client.delete(params['url'].format(id=str(params['perm'].id)), headers={"Authorization": access})
    deleted_perm = session.query(Permission).filter_by(id=id_perm).all()
    assert len(deleted_perm) == 0
    if len(deleted_perm) != 0:
        session.delete(params['perm'])
        session.commit()
    session.delete(params['role'])
    session.delete(params['perm_obj'])
    session.commit()
