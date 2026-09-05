def test_create_order(client):
    payload = {
        "customer_id": 1,
        "dining_table_id": 2,
        "items": [
            {
                "menu_item_id": 1,
                "quantity": 2
            }
        ]
    }

    response = client.post("/orders", json=payload)

    assert response.status_code == 201

    order = response.get_json()

    assert order["total_cents"] == 398


def test_unavailable_item(client):
    payload = {
        "customer_id": 1,
        "dining_table_id": 2,
        "items": [
            {
                "menu_item_id": 5,
                "quantity": 1
            }
        ]
    }

    response = client.post("/orders", json=payload)

    assert response.status_code == 400


def test_order_status_flow(client):
    payload = {
        "customer_id": 1,
        "dining_table_id": 2,
        "items": [
            {
                "menu_item_id": 1,
                "quantity": 1
            }
        ]
    }

    create = client.post("/orders", json=payload)

    order_id = create.get_json()["order_id"]

    r1 = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "PREPARING"}
    )

    assert r1.status_code == 200

    r2 = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "READY"}
    )

    assert r2.status_code == 200

    r3 = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "COMPLETED"}
    )

    assert r3.status_code == 200