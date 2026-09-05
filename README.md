# Restaurant OpenAPI + SQLite Interface Harness

A reusable **Flask + SQLite** backend that implements the Restaurant OpenAPI contract with automated contract validation, business-rule testing, and a deterministic SQLite test harness.

---

## Project Structure

```text
restaurant-api/
├── openapi.yaml
├── schema.sql
├── seed.sql
├── requirements.txt
├── run-tests.sh
├── README.md
│
├── src/
│   ├── app.py
│   ├── db.py
│   └── handlers.py
│
├── harness/
│   ├── contract.py
│   ├── reset_db.py
│   └── validate_openapi.py
│
└── tests/
    ├── conftest.py
    ├── test_menu.py
    ├── test_reservations.py
    ├── test_orders.py
    ├── test_contract.py
    ├── test_http_contract.py
    └── test_fresh_db.py
```

---

## Features

* OpenAPI-first REST API
* Flask + SQLite backend
* 10 implemented endpoints
* Reusable contract validation harness
* Database reset utility
* Automated business & contract tests
* One-command test execution

---

## Requirements

* Python 3.10+
* SQLite (built into Python)

Install dependencies:

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
pip install -r requirements.txt
```

---

## Database

Create a fresh database anytime:

```bash
python harness/reset_db.py
```

This recreates `restaurant.db` using `schema.sql` and `seed.sql`.

---

## Validate OpenAPI

```bash
python harness/validate_openapi.py
```

Expected output:

```text
PASS: OpenAPI specification is valid
```

---

## Run the Server

```bash
cd src
python app.py
```

Server:

```text
http://127.0.0.1:5000
```

---

## Run All Tests

From the project root:

```bash
./run-tests.sh
```

Expected:

```text
PASS: Fresh SQLite database created
PASS: OpenAPI specification is valid
14 passed

PASS: ALL ACCEPTANCE TESTS PASSED
```

---

## API Endpoints

| Method | Endpoint                 |
| ------ | ------------------------ |
| GET    | `/menu`                  |
| GET    | `/menu/{id}`             |
| POST   | `/customers`             |
| GET    | `/tables`                |
| POST   | `/reservations`          |
| GET    | `/reservations/{id}`     |
| POST   | `/orders`                |
| GET    | `/orders/{id}`           |
| PATCH  | `/orders/{id}/status`    |
| GET    | `/customers/{id}/orders` |

---

## Inspect the API

Example using `curl`:

```bash
curl http://127.0.0.1:5000/menu
```

Or test every endpoint with Postman.

---

## Add a New Endpoint

1. Update `openapi.yaml`
2. Implement the handler in `src/handlers.py`
3. Register the route in `src/app.py`
4. Add a pytest test
5. Run `./run-tests.sh`

---

## Dogfood Workflow

A new developer should be able to complete this workflow using only this README:

1. Reset the database
2. Start the Flask server
3. GET `/menu`
4. POST `/customers`
5. GET `/tables`
6. POST `/reservations`
7. POST `/orders`
8. GET `/orders/{id}`
9. PATCH `/orders/{id}/status`
10. GET `/customers/{id}/orders`
11. Run `./run-tests.sh`

Successful completion indicates the project is functioning correctly.

---

## Author

**Faisal Naseer**

* Email: [Xtfaisal07@gmail.com](mailto:Xtfaisal07@gmail.com)
