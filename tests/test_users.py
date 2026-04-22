# tests/test_users.py

def test_create_user(client):
    user_data ={
        "name": "Sharad Shinde",
        "email": "sharad@example.com",
        "username": "sharad_pro",
        "password": "supersecretpassword123"
    }

    # 2. Send the POST request to your router
    res = client.post("/users", json=user_data)

    #Verify the server accepted it
    assert res.status_code == 201

    # 4. Verify the database returned the correct email (and hid the password!)
    new_user = res.json()
    assert new_user["email"] == "sharad@example.com"
    assert "password" not in new_user

