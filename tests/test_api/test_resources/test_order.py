from fastapi.testclient import TestClient
from routes.api_utils import oauth2_bearer
from src.fastapi_app import app
from datetime import timedelta
from routes.login import create_access_token


client = TestClient(app)


def token_generator():
    token = create_access_token("Admin", "pratiksha15@gmail.com", timedelta(minutes=15))
    return token


def test_place_order():
    app.dependency_overrides[oauth2_bearer] = token_generator
    response = client.post(
        "/orders", json={"orders": [{"product_id": 4, "product_quantity": 2}]}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Order Placed Successfully!"


def test_place_order_fail():
    app.dependency_overrides[oauth2_bearer] = token_generator
    response = client.post("/orders", json={"orders":[]})
    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "Please select atleast one product to place order"
    )


def test_fetch_orders():
    app.dependency_overrides[oauth2_bearer] = token_generator
    response = client.get("/orders")
    assert response.status_code == 200
    # assert len(response.json()) > 0
