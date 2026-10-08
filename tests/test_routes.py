from flask.testing import FlaskClient
from opengeodeweb_back.typed_route import TYPED_ROUTE_MARKER

from tests.conftest import app


def test_allowed_files(client: FlaskClient) -> None:
    route = "/opengeodeweb_back/allowed_files"
    response = client.post(route)
    assert response.status_code == 200


def test_root(client: FlaskClient) -> None:
    route = "/"
    response = client.post(route)
    assert response.status_code == 200


def test_packages_versions(client: FlaskClient) -> None:
    route = "/vease_back/packages_versions"
    response = client.get(route)
    assert response.status_code == 200
    assert response.json is not None
    packages_versions = response.json["packages_versions"]
    assert type(packages_versions) is list
    for version in packages_versions:
        assert type(version) is dict


def test_microservice_version(client: FlaskClient) -> None:
    route = "/vease_back/microservice_version"
    response = client.get(route)
    assert response.status_code == 200
    assert response.json is not None
    microservice_version = response.json["microservice_version"]
    assert type(microservice_version) is str


def test_healthcheck(client: FlaskClient) -> None:
    route = "/vease_back/healthcheck"
    response = client.get(route)
    assert response.status_code == 200
    assert response.json is not None
    message = response.json["message"]
    assert type(message) is str
    assert message == "healthy"


def test_every_route_is_typed() -> None:
    for endpoint, view in app.view_functions.items():
        if endpoint.split(".")[0] != "vease":
            continue
        assert getattr(view, TYPED_ROUTE_MARKER, False), (
            f"{endpoint} must be registered with @typed_route or @raw_route"
        )
