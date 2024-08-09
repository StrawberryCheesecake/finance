from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

@app.route("/test/")
def api_test():
    return [123,"hello world"]