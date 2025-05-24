# tests/test_users.py
def test_create_and_read_user(client):
    # Create
    res = client.post("/api/v1/users/", json={"email": "a@b.com"})
    assert res.status_code == 200
    user = res.json()
    assert user["email"] == "a@b.com"
    user_id = user["id"]

    # List
    res = client.get("/api/v1/users/")
    assert res.status_code == 200
    assert any(u["id"] == user_id for u in res.json())

    # Read
    res = client.get(f"/api/v1/users/{user_id}")
    assert res.status_code == 200
    assert res.json()["email"] == "a@b.com"
