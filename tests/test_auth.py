# tests/test_auth.py

def test_login_success(client, test_user):

    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]}
        )

    assert res.status_code == 200

    token_data = res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_login_incorrect_password(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": "wrongpassword"}
    )

    assert res.status_code == 403

