# Standard library imports
import os

# Third party imports
import flask
import flask_cors
import json
from opengeodeweb_microservice.schemas import get_schemas_dict
from opengeodeweb_back import utils_functions

schemas_dict = get_schemas_dict(os.path.join(os.path.dirname(__file__), "schemas"))

routes = flask.Blueprint("vease_routes", __name__)
flask_cors.CORS(routes)


@routes.route(
    schemas_dict["packages_versions"]["route"],
    methods=schemas_dict["packages_versions"]["methods"],
)
def packages_versions() -> flask.Response:
    utils_functions.validate_request(flask.request, schemas_dict["packages_versions"])
    list_packages = [
        "OpenGeode-core",
        "OpenGeode-Geosciences",
        "OpenGeode-GeosciencesIO",
        "OpenGeode-Inspector",
        "OpenGeode-IO",
        "Geode-Viewables",
    ]
    return flask.make_response(
        {"packages_versions": utils_functions.versions(list_packages)}, 200
    )


@routes.route(
    schemas_dict["microservice_version"]["route"],
    methods=schemas_dict["microservice_version"]["methods"],
)
def microservice_version() -> flask.Response:
    utils_functions.validate_request(
        flask.request, schemas_dict["microservice_version"]
    )
    list_packages = ["vease-back"]
    return flask.make_response(
        {"microservice_version": utils_functions.versions(list_packages)[0]["version"]},
        200,
    )


@routes.route(
    schemas_dict["healthcheck"]["route"], methods=schemas_dict["healthcheck"]["methods"]
)
def healthcheck() -> flask.Response:
    return flask.make_response({"message": "healthy"}, 200)
