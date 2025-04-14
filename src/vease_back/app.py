# Global packages
import argparse
import os

# Third parties
import flask
import flask_cors
from flask_cors import cross_origin
from opengeodeweb_back import utils_functions, app_config
from opengeodeweb_back.routes import blueprint_routes
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import HTTPException

# Local libraries
import vease_back.routes.blueprint_vease as blueprint_vease

""" Global config """
app = flask.Flask(__name__)

""" Config variables """
FLASK_DEBUG = True if os.environ.get("FLASK_DEBUG", default=None) == "True" else False

if FLASK_DEBUG == False:
    app.config.from_object(app_config.ProdConfig)
else:
    app.config.from_object(app_config.DevConfig)

DEFAULT_HOST = app.config.get("DEFAULT_HOST")
DEFAULT_PORT = int(app.config.get("DEFAULT_PORT"))
DEFAULT_DATA_FOLDER_PATH = app.config.get("DEFAULT_DATA_FOLDER_PATH")
ORIGINS = app.config.get("ORIGINS")
TIMEOUT = int(app.config.get("MINUTES_BEFORE_TIMEOUT"))
SSL = app.config.get("SSL")
SECONDS_BETWEEN_SHUTDOWNS = float(app.config.get("SECONDS_BETWEEN_SHUTDOWNS"))

app.register_blueprint(
    blueprint_routes.routes,
    url_prefix="/opengeodeweb_back",
    name="opengeodeweb_back",
)

app.register_blueprint(
    blueprint_vease.routes,
    url_prefix="/vease_back",
    name="vease",
)

if FLASK_DEBUG == False:
    utils_functions.set_interval(utils_functions.kill_task, SECONDS_BETWEEN_SHUTDOWNS, app)

@app.errorhandler(HTTPException)
def errorhandler(e):
    return utils_functions.handle_exception(e)

@app.route("/", methods=["POST"])
@cross_origin()
def root():
    return flask.make_response({}, 200)

def run_server():
    parser = argparse.ArgumentParser(prog='Vease-Back', description='Backend server for Vease')
    parser.add_argument('--host', type=str, default=DEFAULT_HOST, help='Host to run on')
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT, help='Port to listen on')
    parser.add_argument('-d', '--debug', default=FLASK_DEBUG, help='Whether to run in debug mode', action='store_true')
    parser.add_argument('-dfp', '--data_folder_path', type=str, default=DEFAULT_DATA_FOLDER_PATH, help='Path to the folder where data is stored')
    parser.add_argument('-origins', '--allowed_origins', default=ORIGINS, help='Origins that are allowed to connect to the server')
    parser.add_argument('-t', '--timeout', default=TIMEOUT, help='Number of minutes before the server times out')
    args = parser.parse_args()
    app.config.update(DATA_FOLDER_PATH=args.data_folder_path)
    app.config.update(MINUTES_BEFORE_TIMEOUT=args.timeout)
    flask_cors.CORS(app, origins=args.allowed_origins)
    print(f"Host: {args.host}, Port: {args.port}, Debug: {args.debug}, Data folder path: {args.data_folder_path}, Timeout: {args.timeout}, Origins: {args.allowed_origins}", flush=True)
    app.run(debug=args.debug, host=args.host, port=args.port, ssl_context=SSL)


# ''' Main '''
if __name__ == "__main__":
    run_server()
