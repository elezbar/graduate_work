def test_login(client, session):
    url = "/api/v1/login"
    request_body = {"username": "username1", "password": "qwerty100500"}
    response = client.post(url, json=request_body)
    response_json = response.json
    assert response_json.get("access")
    assert response_json.get("refresh")
    request_body["password"] = "-1"
    response = client.post(url, json=request_body)
    assert response.status_code == 401
    request_body["username"] = "-1"
    response = client.post(url, json=request_body)
    assert response.status_code == 401
