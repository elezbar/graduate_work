from models.models import User


def test_registration(client, session):
    session.query(User).filter_by(username="test").delete()
    session.commit()
    url = "/api/v1/registration"
    request_body = {"username": "test", "password": "test"}
    response = client.post(url, json=request_body)
    assert response.json["username"] == "test"
    response = client.post(url, json=request_body)
    assert response.status_code == 403
