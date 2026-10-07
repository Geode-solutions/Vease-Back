# Standard library imports

# Third party imports
import flask
from opengeodeweb_back.app import create_app, register_ogw_back_blueprints, run_server

# Local application imports
from vease_back.routes import blueprint_vease


def create_vease_back() -> flask.Flask:
    app = create_app(__name__)
    register_ogw_back_blueprints(app)
    app.register_blueprint(
        blueprint_vease.routes,
        url_prefix="/vease_back",
        name="vease",
    )
    return app


def run_vease_back() -> None:
    app = create_vease_back()
    run_server(app)


if __name__ == "__main__":
    run_vease_back()
