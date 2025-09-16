# conftest.py
import pytest
from fastapi.testclient import TestClient
from main import app, hash_password, users_db
from datetime import datetime

client = TestClient(app)

# Seed users list (all users from seed_data.py)
seed_users = [
    {"id": 1, "username": "john_doe", "email": "john@example.com", "password": "password123", "age": 30, "phone": "+15551234567"},
    {"id": 2, "username": "jane_smith", "email": "jane@example.com", "password": "securepass456", "age": 25, "phone": "+14155551234"},
    {"id": 3, "username": "bob_wilson", "email": "bob@example.com", "password": "mypass789", "age": 35, "phone": None},
    {"id": 4, "username": "alice_johnson", "email": "alice@example.com", "password": "alicepass", "age": 28, "phone": "+12125551234"},
    {"id": 5, "username": "charlie_brown", "email": "charlie@example.com", "password": "charlie123", "age": 22, "phone": None},
    {"id": 6, "username": "test_user", "email": "test.user@example.com", "password": "Test@123", "age": 40, "phone": None},
    {"id": 7, "username": "admin_user", "email": "admin@company.com", "password": "Admin@2024", "age": 45, "phone": "+19175551234"},
    {"id": 8, "username": "max_age", "email": "maxage@example.com", "password": "maxage123", "age": 150, "phone": None},
    {"id": 9, "username": "min_age", "email": "minage@example.com", "password": "minage123", "age": 18, "phone": None},
    {"id": 10, "username": "very_long_username_that_is_close_to_fifty_chars", "email": "longuser@example.com", "password": "longpass123", "age": 30, "phone": None},
]

@pytest.fixture(scope="session")
def seed_users_db():
    """
    Fixture to seed the test database.
    Adds all users before running tests.
    """
    users_db.clear()  # clear DB first
    for user in seed_users:
        users_db[user["username"].lower()] = {
            "id": user["id"],
            "username": user["username"].lower(),
            "email": user["email"],
            "password": hash_password(user["password"]),  # password should be hashed
            "age": user["age"],
            "phone": user["phone"],
            "created_at": datetime.now(),
            "is_active": True,
            "last_login": None,
        }
    return users_db

@pytest.fixture
def client_with_seed(seed_users_db):
    """
    TestClient fixture with seeded DB.
    """
    return client
