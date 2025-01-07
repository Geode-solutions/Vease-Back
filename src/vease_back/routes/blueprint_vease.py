# Standard library imports
import os

# Third party imports
import flask
import flask_cors
import json
from opengeodeweb_back import utils_functions

schemas = os.path.join(os.path.dirname(__file__), "schemas")

with open(os.path.join(schemas, "versions.json"), "r") as file:
    vease_versions_json = json.load(file)


routes = flask.Blueprint("vease_routes", __name__)
flask_cors.CORS(routes)



@routes.route(
    vease_versions_json["route"], methods=vease_versions_json["methods"]
)
def versions():
    utils_functions.validate_request(flask.request, vease_versions_json)
    list_packages = [
        "OpenGeode-core",
        "OpenGeode-IO",
        "OpenGeode-Inspector",
        "OpenGeode-Geosciences",
        "OpenGeode-GeosciencesIO",
        "Geode-Viewables",
        "Geode-Numerics",
        "Geode-Simplex",
        "Geode-Explicit",
        "Geode-Implicit",
        "Geode-Common",
    ]
    return flask.make_response(
        {"versions": utils_functions.versions(list_packages)}, 200
    )
