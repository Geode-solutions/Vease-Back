# Standard library imports
import time
import shutil
import os
from pathlib import Path
from typing import Generator
import pytest
from flask.testing import FlaskClient

# Local application imports
from vease_back.app import app
from opengeodeweb_microservice.database.connection import init_database, get_session
from opengeodeweb_microservice.database.data import Data

TEST_ID = "1"


@pytest.fixture(scope="session", autouse=True)
def configure_test_environment() -> Generator[None, None, None]:
    base_path = Path(__file__).parent
    test_data_path = base_path / "data"
    data_folder = "./data/"

    shutil.rmtree(data_folder, ignore_errors=True)
    if test_data_path.exists():
        shutil.copytree(test_data_path, f"{data_folder}{TEST_ID}/", dirs_exist_ok=True)

    # Configure app for testing
    app.config["TESTING"] = True
    app.config["SERVER_NAME"] = "TEST"
    app.config["DATA_FOLDER_PATH"] = data_folder
    app.config["UPLOAD_FOLDER"] = "./tests/data/"

    db_path = os.path.join(data_folder, "project.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    init_database(db_path)
    os.environ["TEST_DB_PATH"] = str(db_path)

    yield

    if os.path.exists(data_folder):
        shutil.rmtree(data_folder, ignore_errors=True)


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    app.config["REQUEST_COUNTER"] = 0
    app.config["LAST_REQUEST_TIME"] = time.time()
    client = app.test_client()
    client.environ_base.update(
        {
            "HTTP_CONTENT_TYPE": "application/json",
            "HTTP_ACCEPT": "application/json",
        }
    )
    yield client


@pytest.fixture(autouse=True)
def clean_database() -> Generator[None, None, None]:
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
def app_context() -> Generator[None, None, None]:
    with app.app_context():
        yield


@pytest.fixture
def test_id() -> str:
    return TEST_ID
