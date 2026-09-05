from harness.contract import validate_body

def test_get_customer_orders_matches_contract(client):
    response = client.get("/customers/1/orders")

    assert response.status_code == 200

    validate_body(
        "CustomerOrdersResponse",
        response.get_json()
    )