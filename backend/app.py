from flask import Flask
from flask_cors import CORS
from src.api_managers import ticker_manager

def create_app():
    app = Flask(__name__)

    # Initialize CORS for the entire app
    CORS(app)

    # Register blueprints
    app.register_blueprint(ticker_manager.manage_tick_bp)

    return app

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

@app.route("/test")
def api_test():
    return [123,"hello world"]