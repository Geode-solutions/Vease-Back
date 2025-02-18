# Standard library imports
import os

# Third party imports
import flask
import flask_cors
import json
from opengeodeweb_back import utils_functions

schemas = os.path.join(os.path.dirname(__file__), "schemas")

with open(os.path.join(schemas, "packages_versions.json"), "r") as file:
    packages_versions_json = json.load(file)

with open(os.path.join(schemas, "microservice_version.json"), "r") as file:
    microservice_version_json = json.load(file)

with open(os.path.join(schemas, "healthcheck.json"), "r") as file:
    healthcheck_json = json.load(file)


routes = flask.Blueprint("vease_routes", __name__)
flask_cors.CORS(routes)


@routes.route(
    packages_versions_json["route"], methods=packages_versions_json["methods"]
)
def packages_versions():
    utils_functions.validate_request(flask.request, packages_versions_json)
    list_packages = [
        "OpenGeode-core",
        "OpenGeode-Geosciences",
        "OpenGeode-GeosciencesIO",
        "OpenGeode-Inspector",
        "OpenGeode-IO",
        "Geode-Background",
        "Geode-Common",
        "Geode-Conversion",
        "Geode-Explicit",
        "Geode-Implicit",
        "Geode-Numerics",
        "Geode-Simplex",
        "Geode-Viewables",
    ]
    return flask.make_response(
        {"packages_versions": utils_functions.versions(list_packages)}, 200
    )


@routes.route(
    microservice_version_json["route"], methods=microservice_version_json["methods"]
)
def microservice_version():
    utils_functions.validate_request(flask.request, microservice_version_json)
    list_packages = ["vease-back"]
    return flask.make_response(
        {"microservice_version": utils_functions.versions(list_packages)[0]["version"]},
        200,
    )


@routes.route(healthcheck_json["route"], methods=healthcheck_json["methods"])
def healthcheck():
    return flask.make_response({"message": "healthy"}, 200)
