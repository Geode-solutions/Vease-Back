import pytest
from src.geodeapp_back.app import app, run_server


@pytest.fixture
def client():
    print("app", app, flush=True)
    app.config["TESTING"] = True
    app.config["SERVER_NAME"] = "TEST"
    app.config["DATA_FOLDER"] = "./data/"
    client = app.test_client()
    # client = run_server()
    client.headers = {"Content-type": "application/json", "Accept": "application/json"}
    yield client
