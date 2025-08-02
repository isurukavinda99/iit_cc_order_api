import os
import requests

BASE_URL = "http://localhost:8081/payment/"
HEADERS = {
    "x-amzn-oidc-data": os.environ["OIDC_TOKEN"]
}


def test_make_payment():
    payment_id = "pay_123456789"
    payment_payload = {
        "payment_id": payment_id,
        "payment_date": "2025-07-04T15:30:00",
        "verify_signature": "sig_abcXYZ987654",
        "payment_amount": 2500.75,
        "order_id": 5,
        "payment_status": "true"
    }

    response = requests.post(BASE_URL, json=payment_payload, headers=HEADERS)
    assert response.status_code == 200, response.text
    data = response.json()

    # Validate the response structure (modify based on your actual return schema)
    assert data["payment_id"] == payment_id
    assert data["payment_amount"] == 2500.75
