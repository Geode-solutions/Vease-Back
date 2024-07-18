# Global packages
import argparse
import os
import time

# Third parties
import flask
import flask_cors
from opengeodeweb_back import geode_functions
from opengeodeweb_back.routes import blueprint_routes
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import HTTPException

# Local libraries
from geodeapp_back import config


""" Global config """
app = flask.Flask(__name__)


def kill_task():
    if not os.path.exists(LOCK_FOLDER):
        os.mkdir(LOCK_FOLDER)
    if not os.path.exists(TIME_FOLDER):
        os.mkdir(TIME_FOLDER)

    if len(os.listdir(LOCK_FOLDER)) == 0:
        print(f"No files in the {LOCK_FOLDER} folder, shutting down...", flush=True)
        os._exit(0)
    if not os.path.isfile(TIME_FOLDER + "/time.txt"):
        print("'time.txt' file doesn't exist, shutting down...", flush=True)
        os._exit(0)
    if os.path.isfile(TIME_FOLDER + "/time.txt"):
        with open(TIME_FOLDER + "/time.txt", "r") as file:
            try:
                last_request_time = float(file.read())
            except Exception as e:
                print("error : ", str(e), flush=True)
                os._exit(0)
            current_time = time.time()
            if (current_time - last_request_time) / 60 > MINUTES_BEFORE_TIMEOUT:
                print(
                    "Server timed out due to inactivity, shutting down...", flush=True
                )
                os._exit(0)
    if os.path.isfile(LOCK_FOLDER + "/ping.txt"):
        os.remove(LOCK_FOLDER + "/ping.txt")


""" Config variables """
FLASK_DEBUG = True if os.environ.get("FLASK_DEBUG", default=None) == "True" else False


if FLASK_DEBUG == False:
    app.config.from_object(config.ProdConfig)
else:
    app.config.from_object(config.DevConfig)

ID = app.config.get("ID")
DEFAULT_PORT = int(app.config.get("DEFAULT_PORT"))
DEFAULT_DATA_FOLDER_PATH = app.config.get("DEFAULT_DATA_FOLDER_PATH")
ORIGINS = app.config.get("ORIGINS")
SSL = app.config.get("SSL")
LOCK_FOLDER = app.config.get("LOCK_FOLDER")
TIME_FOLDER = app.config.get("TIME_FOLDER")
MINUTES_BEFORE_TIMEOUT = float(app.config.get("MINUTES_BEFORE_TIMEOUT"))
SECONDS_BETWEEN_SHUTDOWNS = float(app.config.get("SECONDS_BETWEEN_SHUTDOWNS"))


app.register_blueprint(
    blueprint_routes.routes,
    url_prefix="/opengeodeweb_back",
    name="opengeodeweb_back",
)

if FLASK_DEBUG == False:
    geode_functions.set_interval(kill_task, SECONDS_BETWEEN_SHUTDOWNS)
flask_cors.CORS(app, origins=ORIGINS)


@app.errorhandler(HTTPException)
def errorhandler(e):
    return geode_functions.handle_exception(e)

@app.route("/", methods=["POST"])
def root():
    return flask.make_response({"ID": str("123456")}, 200)

@app.route("/ping", methods=["POST"])
def ping():
    LOCK_FOLDER = flask.current_app.config["LOCK_FOLDER"]
    if not os.path.exists(LOCK_FOLDER):
        os.mkdir(LOCK_FOLDER)
    if not os.path.isfile(LOCK_FOLDER + "/ping.txt"):
        f = open(LOCK_FOLDER + "/ping.txt", "a")
        f.close()
    return flask.make_response({"message": "Flask server is running"}, 200)


def run_server():
    parser = argparse.ArgumentParser(prog='GeodeApp-Back', description='Backend server for GeodeApp')
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT, help='Port to listen on')
    parser.add_argument('-d', '--debug', default=FLASK_DEBUG, help='Whether to run in debug mode', action='store_true')
    parser.add_argument('-dfp', '--data_folder_path', type=str, default=DEFAULT_DATA_FOLDER_PATH, help='Path to the folder where data is stored')
    args = parser.parse_args()
    app.config.update(DATA_FOLDER_PATH=args.data_folder_path)
    print(f"Port: {args.port}, Debug: {args.debug}, Data folder path: {args.data_folder_path}", flush=True)
    app.run(debug=args.debug, host="0.0.0.0", port=args.port, ssl_context=SSL)


# ''' Main '''
if __name__ == "__main__":
    run_server()
