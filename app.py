from src.geodeapp_back.app import app

if __name__ == "__main__":
    app.run(debug=app.config.get("FLASK_DEBUG"))
