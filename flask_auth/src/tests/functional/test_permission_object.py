import pytest

from models.models import PermissionObject


@pytest.fixture()
def params(session):
    url = '/api/v1/permission_object/{name}'
    name = 'TestPermissionObject'
    perm = PermissionObject(name=name)
    session.add(perm)
    session.commit()
    return {'url': url, 'name': name, 'perm': perm}


def test_get_permission_object(client, session, access, params):
    response = client.get(params['url'].format(name=params['name']), headers={"Authorization": access})
    response_json = response.json
    session.delete(params['perm'])
    session.commit()
    assert response_json.get("name") == params['name']


def test_delete_permission_object(client, session, access, params):
    client.delete(params['url'].format(name=params['name']), headers={"Authorization": access})
    deleted_perm = session.query(PermissionObject).filter_by(name=params['name']).all()
    assert len(deleted_perm) == 0
    if len(deleted_perm) != 0:
        session.delete(params['perm'])
        session.commit()
