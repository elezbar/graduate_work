import pytest

from models.models import Role


@pytest.fixture()
def params(session):
    url = "/api/v1/role/{name}"
    name = "TestRole"
    role = Role(name=name)
    session.add(role)
    session.commit()
    return {'url': url, 'role': role, 'name': name}


def test_get_role(client, session, access, params):
    response = client.get(params['url'].format(name=params['name']), headers={"Authorization": access})
    response_json = response.json
    session.delete(params['role'])
    session.commit()
    assert response_json.get("name") == params['name']


def test_delete_role(client, session, access, params):
    client.delete(params['url'].format(name=params['name']), headers={"Authorization": access})
    deleted_role = session.query(Role).filter_by(name=params['name']).all()
    assert len(deleted_role) == 0
    if len(deleted_role) != 0:
        session.delete(params['role'])
        session.commit()
