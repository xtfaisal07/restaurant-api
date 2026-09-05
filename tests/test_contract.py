import pytest
from harness.contract import validate_body

def test_valid_customer_response():
    body = {
        "id": 1,
        "name": "Alice",
        "email": "alice@test.com",
        "phone": "9999999999"
    }

    assert validate_body("Customer", body)


def test_contract_judge_invalid_response():
    """
    A3:
    Intentionally remove required fields.
    Harness must reject the response.
    """
    bad = {
        "id": 1,
        "name": "Alice"
    }

    with pytest.raises(Exception):
        validate_body("Customer", bad)