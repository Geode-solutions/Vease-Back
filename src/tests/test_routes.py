def test_allowed_files(client):
    route = f"/opengeodeweb_back/allowed_files"
    response = client.post(route, json={"supported_feature": None})
    assert response.status_code == 200


def test_root(client):
    route = f"/"
    response = client.post(route)
    assert response.status_code == 200

def test_versions(client):
    route = f"/vease/versions"
    response = client.get(route)
    assert response.status_code == 200
    versions = response.json["versions"]
    print(type(versions), versions, flush=True)
    assert type(versions) is list
    for version in versions:
        assert type(version) is dict
