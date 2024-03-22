#!/usr/bin/python3
"""Starts a Flask web application.
   Application listens on 0.0.0.0:5000
   The script uses the strict_slashes to false
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Prints 'Hello HBNB!'"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
