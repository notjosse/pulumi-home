from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/josse")
def josse():
    return "<h>Josse!</h1>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)