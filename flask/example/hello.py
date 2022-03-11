import json
from flask import (
    Flask,
    render_template,
    Response,
    abort,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/hello")
@app.route("/hello/<name>")
def hello(name=None):
    if name is None:
        error_text = "Error: No name has been provided"
        response = Response(
            response=error_text,
            status=401,
        )
        app.logger.error(error_text)
        return response

    return f"<p>Hello {name}!</p>"


@app.route("/configuration.json", methods=["GET"])
def configuration():
    conf = {
        "log_file": "test",
        "updated_date": "some date",
    }

    response = Response(
        response=json.dumps(conf),
    )
    response.headers["Content-Type"] = "application/json"

    return response


# Note that there isn't a trailing / so a request to /abort/ will
# generate a 404.
@app.route('/abort')
def abort_request():
    abort(401)
