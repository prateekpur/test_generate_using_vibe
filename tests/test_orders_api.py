from fastapi.testclient import TestClient
from demo_api.app import app

client = TestClient(app)


def test_login_success():
    response = client.post(
        "/auth/login",
        json={
            "email": "user@test.com",
            "password": "secret123",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["access_token"] == "testtoken"


def test_login_invalid_credentials():
    response = client.post(
        "/auth/login",
        json={
            "email": "user@test.com",
            "password": "wrongpass",
        },
    )

    assert response.status_code == 401


def test_create_order_success():
    response = client.post(
        "/orders",
        headers={"Authorization": "Bearer testtoken"},
        json={
            "item_id": "ABC123",
            "quantity": 2,
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["item_id"] == "ABC123"
    assert body["quantity"] == 2
    assert "order_id" in body


def test_create_order_unauthorized():
    response = client.post(
        "/orders",
        json={
            "item_id": "ABC123",
            "quantity": 2,
        },
    )

    assert response.status_code == 401


def test_create_order_business_rule_blocked_item():
    response = client.post(
        "/orders",
        headers={"Authorization": "Bearer testtoken"},
        json={
            "item_id": "BLOCKED",
            "quantity": 1,
        },
    )

    assert response.status_code == 400
