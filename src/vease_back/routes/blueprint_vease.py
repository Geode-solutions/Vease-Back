# Standard library imports

# Third party imports
import flask
import flask_cors  # type: ignore[import-untyped]
from opengeodeweb_back import utils_functions
from opengeodeweb_back.typed_route import typed_route

# Local application imports
from vease_back.routes import schemas

routes = flask.Blueprint("vease_routes", __name__)
flask_cors.CORS(routes)


@typed_route(routes, schemas.packages_versions_route)
def packages_versions(
    _params: schemas.PackagesVersions,
) -> schemas.PackagesVersionsResponse:
    list_packages = [
        "OpenGeode-core",
        "OpenGeode-Geosciences",
        "OpenGeode-GeosciencesIO",
        "OpenGeode-Inspector",
        "OpenGeode-IO",
        "Geode-Viewables",
    ]
    return schemas.PackagesVersionsResponse(
        packages_versions=[
            schemas.packages_versions.PackagesVersion(
                package=version["package"], version=version["version"]
            )
            for version in utils_functions.versions(list_packages)
        ]
    )


@typed_route(routes, schemas.microservice_version_route)
def microservice_version(
    _params: schemas.MicroserviceVersion,
) -> schemas.MicroserviceVersionResponse:
    list_packages = ["vease-back"]
    return schemas.MicroserviceVersionResponse(
        microservice_version=utils_functions.versions(list_packages)[0]["version"]
    )


@typed_route(routes, schemas.healthcheck_route)
def healthcheck(_params: schemas.Healthcheck) -> schemas.HealthcheckResponse:
    return schemas.HealthcheckResponse(message="healthy")
