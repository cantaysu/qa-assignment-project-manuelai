# tests/test_users.py
import pytest

# ----------------- HELPER FUNCTIONS -----------------
def get_token(client, username="john_doe", password="password123"):
    print(f"Logging in as {username}")
    response = client.post("/login", json={"username": username, "password": password})
    assert response.status_code == 200, f"Login failed for {username}"
    token = response.json()["token"]
    print(f"Token received: {token[:10]}...")  # show only the first 10 characters
    return token

# ----------------- POSITIVE SCENARIOS -----------------
def test_login_success(client_with_seed):
    print("1 - Login: Attempting login with correct credentials")
    response = client_with_seed.post(
        "/login",
        json={"username": "jane_smith", "password": "securepass456"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user_id"] == 2
    print("Login successful\n")

def test_create_user_success(client_with_seed):
    print("2 - Create User: Creating a new user")
    token = get_token(client_with_seed)
    headers = {"Authorization": f"Bearer {token}"}

    new_user = {
        "username": "new_user_test",
        "email": "new_user_test@example.com",
        "password": "NewPass123",
        "age": 27,
        "phone": "+1234567890"
    }
    response = client_with_seed.post("/users", json=new_user, headers=headers)
    assert response.status_code == 201
    assert response.json()["username"] == new_user["username"]
    print("New user created successfully\n")

def test_get_user_list(client_with_seed):
    print("3 - Get User List: Retrieving all users")
    response = client_with_seed.get("/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 10
    print(f"Retrieved {len(users)} users\n")

def test_get_user_by_id(client_with_seed):
    print("4 - Get User by ID: Retrieving user with ID 1")
    response = client_with_seed.get("/users/1")
    assert response.status_code == 200
    user = response.json()
    assert user["username"] == "john_doe"
    print(f"User retrieved: {user['username']}\n")

def test_update_user_success(client_with_seed):
    print("5 - Update User: Updating an existing user")
    token = get_token(client_with_seed)
    headers = {"Authorization": f"Bearer {token}"}

    new_user = {
        "username": "update_user_test",
        "email": "update_user_test@example.com",
        "password": "Update123",
        "age": 26
    }
    create_resp = client_with_seed.post("/users", json=new_user, headers=headers)
    user_id = create_resp.json()["id"]
    print(f"Created user with ID {user_id} for update")

    update_data = {"email": "updated@example.com", "age": 27}
    update_resp = client_with_seed.put(f"/users/{user_id}", json=update_data, headers=headers)
    assert update_resp.status_code == 200
    updated_user = update_resp.json()
    assert updated_user["email"] == update_data["email"]
    assert updated_user["age"] == update_data["age"]
    print("User updated successfully\n")

def test_delete_existing_user(client_with_seed):
    print("6 - Delete User: Deleting an existing user")
    token = get_token(client_with_seed)
    headers = {"Authorization": f"Bearer {token}"}

    new_user = {
        "username": "temp_user_test",
        "email": "temp_user_test@example.com",
        "password": "Temp123",
        "age": 30
    }
    create_resp = client_with_seed.post("/users", json=new_user, headers=headers)
    user_id = create_resp.json()["id"]
    print(f"Created user with ID {user_id} for deletion")

    delete_resp = client_with_seed.delete(f"/users/{user_id}", headers=headers)
    assert delete_resp.status_code == 200
    assert delete_resp.json()["was_active"] is True
    print("User deleted successfully\n")

# ----------------- NEGATIVE SCENARIOS -----------------
def test_login_wrong_password(client_with_seed):
    print("7 - Login Failure: Attempting login with wrong password")
    response = client_with_seed.post(
        "/login",
        json={"username": "jane_smith", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"
    print("Login failed as expected\n")

def test_login_nonexistent_user(client_with_seed):
    print("8 - Login Failure: Attempting login for non-existent user")
    response = client_with_seed.post(
        "/login",
        json={"username": "ghost", "password": "any"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"
    print("Login failed as expected\n")

def test_create_user_existing_username(client_with_seed):
    print("9 - Create User Failure: Attempting to create user with existing username")
    token = get_token(client_with_seed)
    headers = {"Authorization": f"Bearer {token}"}

    user = {
        "username": "john_doe",
        "email": "john_new@test.com",
        "password": "newpass123",
        "age": 25
    }
    response = client_with_seed.post("/users", json=user, headers=headers)
    assert response.status_code == 400
    assert "Username already exists" in response.text
    print("User creation failed as expected\n")

def test_create_user_missing_fields(client_with_seed):
    print("10 - Create User Failure: Missing required fields")
    token = get_token(client_with_seed)
    headers = {"Authorization": f"Bearer {token}"}

    user = {"username": "incomplete"}
    response = client_with_seed.post("/users", json=user, headers=headers)
    assert response.status_code == 422
    print("User creation failed due to missing fields\n")

def test_update_user_unauthorized(client_with_seed):
    print("11 - Update User Failure: Attempting update without authentication")
    response = client_with_seed.put("/users/1", json={"age": 50})
    assert response.status_code == 401
    print("Update failed as expected\n")

def test_delete_user_unauthorized(client_with_seed):
    print("12 - Delete User Failure: Attempting deletion without authentication")
    response = client_with_seed.delete("/users/1")
    assert response.status_code == 401
    print("Deletion failed as expected\n")

def test_delete_nonexistent_user(client_with_seed):
    print("13 - Delete User Failure: Attempting to delete a non-existent user")
    token = get_token(client_with_seed)
    headers = {"Authorization": f"Bearer {token}"}

    response = client_with_seed.delete("/users/99999", headers=headers)
    assert response.status_code == 404
    print("Deletion failed as expected\n")
