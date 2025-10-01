import pytest
import os
from typing import Generator
from src.vease_back.app import app
from opengeodeweb_microservice.database.connection import (
    init_database as init_db_connection,
    get_session,
)
from opengeodeweb_microservice.database.data import Data


DB_PATH: str = os.path.join(os.path.dirname(__file__), "test_project.db")


@pytest.fixture(scope="session", autouse=True)
def client():
    app.config["TESTING"] = True
    app.config["SERVER_NAME"] = "TEST"
    app.config["DATA_FOLDER"] = "./data/"
    client = app.test_client()
    client.headers = {"Content-type": "application/json", "Accept": "application/json"}
    yield client


@pytest.fixture(autouse=True)
def clean_database() -> Generator[None, None, None]:
    session = get_session()
    if session is not None:
        session.query(Data).delete()
        session.commit()
    yield
    try:
        if session is not None:
            session.rollback()
    except Exception:
        pass


@pytest.fixture(scope="session", autouse=True)
def setup_database() -> Generator[None, None, None]:
    init_db_connection(DB_PATH)
    yield
    _cleanup_database(DB_PATH)


def _cleanup_database(db_path: str) -> None:
    try:
        session = get_session()
        if session is not None:
            session.close()
    except Exception:
        pass

    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            pass
