# Restaurant OpenAPI + SQLite Interface Harness

Reusable Flask + SQLite backend implementing the Restaurant OpenAPI contract.

## Requirements

- Python 3.10+
- Flask
- SQLite
- pytest
- openapi-core

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Reset Database

```bash
python harness/reset_db.py
```

## Validate OpenAPI

```bash
python harness/validate_openapi.py
```

## Run Server

```bash
cd src
python app.py
```

Server runs at:

http://127.0.0.1:5000

## Run Complete Harness

```bash
./run-tests.sh
```

---

# Canonical Fresher Workflow

1. Reset database
2. GET `/menu`
3. POST `/customers`
4. GET `/tables`
5. POST `/reservations`
6. POST `/orders`
7. GET `/orders/{id}`
8. PATCH `/orders/{id}/status`
9. GET `/customers/{id}/orders`
10. Run `./run-tests.sh`

Expected result: All tests PASS.

## Implemented Endpoints

- GET /menu
- GET /menu/{id}
- POST /customers
- GET /tables
- POST /reservations
- GET /reservations/{id}
- POST /orders
- GET /orders/{id}
- PATCH /orders/{id}/status
- GET /customers/{id}/orders

## Dogfood Acceptance Test

Follow these steps without reading the source code:

1. python harness/reset_db.py
2. GET /menu
3. POST /customers
4. GET /tables
5. POST /reservations
6. POST /orders
7. GET /orders/{id}
8. PATCH /orders/{id}/status
9. GET /customers/{id}/orders
10. ./run-tests.sh

Expected result: PASS

## Inspect API

Use Postman or curl.

Example:

```bash
curl http://127.0.0.1:5000/menu
```

## Add a New Endpoint

1. Add schema/path to `openapi.yaml`
2. Implement handler in `handlers.py`
3. Register route in `app.py`
4. Add pytest
5. Run `./run-tests.sh`