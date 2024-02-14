from fastapi.testclient import TestClient
from routes.api_utils import oauth2_bearer
from src.fastapi_app import app
from datetime import timedelta
from routes.login import create_access_token


client = TestClient(app)


def token_generator():
    token = create_access_token("Customer", "hello1@gmail.com", timedelta(minutes=15))
    return token


def test_show_wallet():
    app.dependency_overrides[oauth2_bearer] = token_generator
    response = client.get(
        "/wallet"
    )
    assert response.status_code == 200
    assert response.json()["email"] == "hello1@gmail.com"

def test_update_wallet():
    app.dependency_overrides[oauth2_bearer] = token_generator
    response = client.put(
        "/wallet", json={"amount":23}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "hello1@gmail.com"