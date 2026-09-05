def test_create_reservation(client):
    payload = {
        "customer_id": 1,
        "dining_table_id": 2,
        "reservation_time": "2026-09-10T19:00:00",
        "party_size": 2
    }

    response = client.post("/reservations", json=payload)

    assert response.status_code == 201


def test_large_party_rejected(client):
    payload = {
        "customer_id": 1,
        "dining_table_id": 1,
        "reservation_time": "2026-09-10T20:00:00",
        "party_size": 5
    }

    response = client.post("/reservations", json=payload)

    assert response.status_code == 400


def test_duplicate_table_time(client):
    payload = {
        "customer_id": 1,
        "dining_table_id": 2,
        "reservation_time": "2026-09-10T21:00:00",
        "party_size": 2
    }

    client.post("/reservations", json=payload)

    response = client.post("/reservations", json=payload)

    assert response.status_code == 409