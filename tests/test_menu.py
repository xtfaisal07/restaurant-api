def test_list_menu(client):
    response = client.get("/menu")

    assert response.status_code == 200

    data = response.get_json()

    assert "Starters" in data
    assert "Main Course" in data
    assert len(data["Starters"]) > 0


def test_get_menu_item(client):
    response = client.get("/menu/1")

    assert response.status_code == 200

    item = response.get_json()

    assert item["name"] == "Garlic Bread"


def test_menu_404(client):
    response = client.get("/menu/999")

    assert response.status_code == 404