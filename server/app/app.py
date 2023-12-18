from flask import Flask, make_response

app = Flask(__name__)


@app.route("/")
def hello():
    return make_response("hi!")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
