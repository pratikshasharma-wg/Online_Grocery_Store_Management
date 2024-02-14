from fastapi.testclient import TestClient
from routes.api_utils import oauth2_bearer
from src.fastapi_app import app
from datetime import timedelta
from routes.login import create_access_token


client = TestClient(app)


def token_generator():
    token = create_access_token("Admin", "pratiksha15@gmail.com", timedelta(minutes=15))
    return token


def test_register():
    app.dependency_overrides[oauth2_bearer] = token_generator
    response = client.post(
        "/register", json={"name": "abc123", "email": "abc12345@gmail.com", "password": "1234abc@", "wallet_status": 23}
    )
    assert response.status_code == 201
    assert response.json()["message"] == "User with email abc12345@gmail.com registered successfully!"