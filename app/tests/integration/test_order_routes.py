import os
import requests
import uuid

BASE_URL = "http://127.0.0.1:8091/order/"
HEADERS = {
    "x-amzn-oidc-data": os.environ["OIDC_TOKEN"]
}

def test_order_crud_flow():
    # 1. Create order
    create_payload = {
        "game_ids": [
            "123e4567-e89b-12d3-a456-426614174000",
            "987e6543-e21c-43f1-a456-426614174999"
        ],
        "item_prices": [49.99, 19.99],
        "active": "true"
    }

    create_res = requests.post(BASE_URL, json=create_payload, headers=HEADERS)
    assert create_res.status_code == 200, create_res.text
    order = create_res.json()
    order_id = order["id"]

    # 2. Get all orders by status
    list_res = requests.get(BASE_URL, headers=HEADERS, params={"status": "PENDING"})
    assert list_res.status_code == 200, list_res.text
    orders = list_res.json()
    assert any(o["id"] == order_id for o in orders)

    # 3. Get order by ID
    get_res = requests.get(f"{BASE_URL}{order_id}", headers=HEADERS)
    assert get_res.status_code == 200, get_res.text
    fetched = get_res.json()
    assert fetched["id"] == order_id
