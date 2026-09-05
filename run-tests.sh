#!/bin/bash

echo "===================================="
echo " Restaurant OpenAPI Harness"
echo "===================================="

echo ""
echo "[1/3] Resetting SQLite..."
python harness/reset_db.py || exit 1

echo ""
echo "[2/3] Validating OpenAPI..."
python harness/validate_openapi.py || exit 1

echo ""
echo "[3/3] Running Contract + Business Tests..."
pytest -v || exit 1

echo ""
echo "===================================="
echo " PASS: ALL ACCEPTANCE TESTS PASSED"
echo "===================================="