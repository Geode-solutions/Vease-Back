# Standard library imports

# Third party imports
from opengeodeweb_back.app import app, run_server

# Local application imports
import vease_back.routes.blueprint_vease as blueprint_vease


app.register_blueprint(
    blueprint_vease.routes,
    url_prefix="/vease_back",
    name="vease",
)


def run_vease_back() -> None:
    run_server()


if __name__ == "__main__":
    run_vease_back()
