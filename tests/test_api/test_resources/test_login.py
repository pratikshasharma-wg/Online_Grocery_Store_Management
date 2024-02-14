from fastapi.testclient import TestClient
from fastapi import status
import pytest
from datetime import timedelta
from src.fastapi_app import app
from routes.login import create_access_token

client = TestClient(app)


def generate_token(role, username):
    token = create_access_token(role, username, timedelta(minutes=15))
    return {"access_token": token, "message": "User logged in successfully!"}


def test_login_user_admin():
    response = client.post(
        "/login",
        json={"email": "Pratiksha15@gmail.com", "password": "Pratiksha15@Skit"},
    )
    # token = generate_token("Admin", "Pratiksha15@gmail.com", "Pratiksha15@Skit")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "User logged in successfully!"


def test_login_user_customer():
    response = client.post(
        "/login", json={"email": "hello1@gmail.com", "password": "Hello123@"}
    )
    # token = generate_token("Customer", "hello1@gmail.com", "Hello123@")

    assert response.json()["message"] == "User logged in successfully!"
    assert response.status_code == status.HTTP_200_OK


def test_login_user_fail():
    response = client.post(
        "/login", json={"email": "abc@gmail.com", "password": "Hello123@"}
    )
    # token = generate_token("Customer", "abc@gmail.com", "Hello123@")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
