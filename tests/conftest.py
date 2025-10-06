# Standard library imports
import time
import shutil
import os
from pathlib import Path
from typing import Generator

# Third party imports
import pytest

# Local application imports
from vease_back.app import app
from opengeodeweb_microservice.database.connection import init_database, get_session
from opengeodeweb_microservice.database.data import Data

TEST_ID = "1"


@pytest.fixture(scope="session", autouse=True)
def configure_test_environment() -> Generator[None, None, None]:
    base_path = Path(__file__).parent
    test_data_path = base_path / "data"

    # Clean up any existing test data
    shutil.rmtree("./data", ignore_errors=True)
    if test_data_path.exists():
        shutil.copytree(test_data_path, f"./data/{TEST_ID}/", dirs_exist_ok=True)

    # Configure app for testing
    app.config["TESTING"] = True
    app.config["SERVER_NAME"] = "TEST"
    app.config["DATA_FOLDER_PATH"] = "./data/"
    app.config["UPLOAD_FOLDER"] = "./tests/data/"

    # Setup database
    db_filename = "project.db"
    db_dir = os.path.join(base_path, "data")
    db_path = os.path.join(db_dir, db_filename)
    os.makedirs(db_dir, exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    init_database(app, db_filename)
    os.environ["TEST_DB_PATH"] = str(db_path)

    yield

    # Cleanup after tests
    tmp_data_path = app.config.get("DATA_FOLDER_PATH")
    if tmp_data_path and os.path.exists(tmp_data_path):
        shutil.rmtree(tmp_data_path, ignore_errors=True)
        print(f"Cleaned up test data folder: {tmp_data_path}", flush=True)


@pytest.fixture
def client():
    app.config["REQUEST_COUNTER"] = 0
    app.config["LAST_REQUEST_TIME"] = time.time()
    client = app.test_client()
    client.headers = {"Content-type": "application/json", "Accept": "application/json"}
    yield client


@pytest.fixture(autouse=True)
def clean_database():
    with app.app_context():
        session = get_session()
        if session:
            session.query(Data).delete()
            session.commit()
    yield
    with app.app_context():
        try:
            session = get_session()
            if session:
                session.rollback()
        except Exception:
            pass


@pytest.fixture
def app_context():
    with app.app_context():
        yield


@pytest.fixture
def test_id():
    return TEST_ID
