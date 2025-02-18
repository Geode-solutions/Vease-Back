def test_allowed_files(client):
    route = f"/opengeodeweb_back/allowed_files"
    response = client.post(route, json={"supported_feature": None})
    assert response.status_code == 200


def test_root(client):
    route = f"/"
    response = client.post(route)
    assert response.status_code == 200


def test_packages_versions(client):
    route = f"/vease_back/packages_versions"
    response = client.get(route)
    assert response.status_code == 200
    packages_versions = response.json["packages_versions"]
    print(type(packages_versions), packages_versions, flush=True)
    assert type(packages_versions) is list
    for version in packages_versions:
        assert type(version) is dict


def test_microservice_version(client):
    route = f"/vease_back/microservice_version"
    response = client.get(route)
    assert response.status_code == 200
    microservice_version = response.json["microservice_version"]
    print(type(microservice_version), microservice_version, flush=True)
    assert type(microservice_version) is str


def test_healthcheck(client):
    route = f"/vease_back/healthcheck"
    response = client.get(route)
    assert response.status_code == 200
    message = response.json["message"]
    assert type(message) is str
    assert message == "healthy"
