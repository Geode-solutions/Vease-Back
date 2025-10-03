# Standard library imports
import os
import shutil
from pathlib import Path
from typing import Generator

# Third party imports
import pytest

# Local application imports
from opengeodeweb_back import app
from opengeodeweb_microservice.database.connection import init_database, get_session
from opengeodeweb_microservice.database.data import Data

# Test database path
DB_PATH = os.path.join(os.path.dirname(__file__), "test_project.db")


@pytest.fixture(scope="session", autouse=True)
def configure_test_environment() -> Generator[None, None, None]:
    base_path = Path(__file__).parent

    app.config["TESTING"] = True
    app.config["SERVER_NAME"] = "TEST"
    app.config["DATA_FOLDER_PATH"] = "./data/"
    app.config["UPLOAD_FOLDER"] = "./tests/data/"

    init_database(DB_PATH)
    os.environ["TEST_DB_PATH"] = str(DB_PATH)
    print(f"Database initialized at: {DB_PATH}", flush=True)
    yield
    _cleanup_database(DB_PATH)

    tmp_data_path = app.config.get("DATA_FOLDER_PATH")
    if tmp_data_path and os.path.exists(tmp_data_path):
        shutil.rmtree(tmp_data_path, ignore_errors=True)
        print(f"Cleaned up test data folder: {tmp_data_path}", flush=True)


@pytest.fixture
def client():
    app.config["REQUEST_COUNTER"] = 0
    app.config["LAST_REQUEST_TIME"] = 0
    client = app.test_client()
    client.headers = {"Content-type": "application/json", "Accept": "application/json"}
    yield client


@pytest.fixture(autouse=True)
def clean_database():
    session = get_session()
    session.query(Data).delete()
    session.commit()
    yield
    try:
        session.rollback()
    except Exception:
        pass


@pytest.fixture
def app_context():
    with app.app_context():
        yield


def _cleanup_database(db_path: str):
    try:
        session = get_session()
        session.close()
    except Exception:
        pass

    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            pass
