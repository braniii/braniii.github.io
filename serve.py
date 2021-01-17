#!/usr/bin/env python3

"""
DEVELOPMENT ONLY

Serves the site with a development Flask server.
"""

import flask

app = flask.Flask(__name__, static_folder="build/static")


@app.route("/")
def index():
    return flask.send_file("build/index.html")


@app.route("/<path:path>")
def other(path):
    return flask.send_from_directory("build", path)


if __name__ == "__main__":
    app.run(debug=True)
