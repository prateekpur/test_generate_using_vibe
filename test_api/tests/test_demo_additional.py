from fastapi.testclient import TestClient
from demo_api.app import app

client = TestClient(app)


def test_login_validation_errors():
    # invalid email
    r1 = client.post(
        "/auth/login",
        json={"email": "not-an-email", "password": "secret123"},
    )
    assert r1.status_code == 422

    # password too short
    r2 = client.post(
        "/auth/login",
        json={"email": "user@test.com", "password": "short"},
    )
    assert r2.status_code == 422


def test_create_order_validation_errors():
    # quantity too small
    r1 = client.post(
        "/orders",
        headers={"Authorization": "Bearer testtoken"},
        json={"item_id": "X", "quantity": 0},
    )
    assert r1.status_code == 422

    # quantity too large
    r2 = client.post(
        "/orders",
        headers={"Authorization": "Bearer testtoken"},
        json={"item_id": "X", "quantity": 11},
    )
    assert r2.status_code == 422

    # empty item_id
    r3 = client.post(
        "/orders",
        headers={"Authorization": "Bearer testtoken"},
        json={"item_id": "", "quantity": 1},
    )
    assert r3.status_code == 422


def test_authorization_header_variants():
    # missing Bearer prefix
    r1 = client.post(
        "/orders",
        headers={"Authorization": "testtoken"},
        json={"item_id": "ABC", "quantity": 1},
    )
    assert r1.status_code == 401


def test_create_and_get_order_roundtrip():
    # create
    create = client.post(
        "/orders",
        headers={"Authorization": "Bearer testtoken"},
        json={"item_id": "ROUND", "quantity": 3},
    )
    assert create.status_code == 201
    body = create.json()
    assert body["item_id"] == "ROUND"
    order_id = body["order_id"]

    # get existing
    get = client.get(
        f"/orders/{order_id}", headers={"Authorization": "Bearer testtoken"}
    )
    assert get.status_code == 200
    got = get.json()
    assert got["order_id"] == order_id

    # get missing
    missing = client.get(
        "/orders/00000000-0000-0000-0000-000000000000",
        headers={"Authorization": "Bearer testtoken"},
    )
    assert missing.status_code == 404
