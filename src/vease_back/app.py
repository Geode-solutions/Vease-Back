# Standard library imports

# Third party imports
import flask
from opengeodeweb_back.app import create_app, run_server, register_ogw_back_blueprints

# Local application imports
import vease_back.routes.blueprint_vease as blueprint_vease


def run_vease_back() -> flask.Flask:
    app = create_app(__name__)
    register_ogw_back_blueprints(app)
    app.register_blueprint(
        blueprint_vease.routes,
        url_prefix="/vease_back",
        name="vease",
    )
    run_server(app)
    return app


if __name__ == "__main__":
    run_vease_back()
