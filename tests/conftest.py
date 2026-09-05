import sys
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent

# Add project root and src to Python path
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "src"))

from app import app
from harness.reset_db import reset_database


@pytest.fixture
def client():
    reset_database()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client