# Standard library imports
import os
import shutil
import time
from collections.abc import Generator
from pathlib import Path

# Third party imports
import pytest
from flask.testing import FlaskClient
from opengeodeweb_microservice.database.connection import get_session, init_database
from opengeodeweb_microservice.database.data import Data

# Local application imports
from vease_back.app import create_vease_back

TEST_ID = "1"

app = create_vease_back()


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
    app.config["UPLOAD_FOLDER_PATH"] = "./tests/data/"

    db_path = Path(data_folder) / "project.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    init_database(db_path)
    os.environ["TEST_DB_PATH"] = str(db_path)

    yield

    shutil.rmtree(data_folder, ignore_errors=True)


@pytest.fixture
def client() -> FlaskClient:
    app.config["REQUEST_COUNTER"] = 0
    app.config["LAST_REQUEST_TIME"] = time.time()
    client = app.test_client()
    client.environ_base.update(
        {
            "HTTP_CONTENT_TYPE": "application/json",
            "HTTP_ACCEPT": "application/json",
        }
    )
    return client


@pytest.fixture(autouse=True)
def clean_database() -> Generator[None, None, None]:
    with app.app_context():
        session = get_session()
        if session:
            session.query(Data).delete()
            session.commit()
    yield
    with app.app_context():
        session = get_session()
        if session:
            session.rollback()


@pytest.fixture
def app_context() -> Generator[None, None, None]:
    with app.app_context():
        yield


@pytest.fixture
def test_id() -> str:
    return TEST_ID
