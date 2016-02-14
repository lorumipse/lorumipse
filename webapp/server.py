#!/usr/bin/env python

from flask import Flask
import sys
import os
from langmodel.generate import generate_text


port_number = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TEXT_TEMPLATE_DIR = os.path.join(SCRIPT_DIR, "..", "build", "text_template")
STATIC_DIR = os.path.join(SCRIPT_DIR, "static")

app = Flask("lorumipse", static_folder=STATIC_DIR)

@app.route("/")
def root():
    return app.send_static_file("index.html")


@app.route("/generate/init/")
def generate_first_paragraph():
    text = generate_text(TEXT_TEMPLATE_DIR, True)
    return text, 200, {
        "Content-type": "text/json; charset=utf-8"
    }


@app.route("/generate/")
def generate_subsequent_paragraph():
    text = generate_text(TEXT_TEMPLATE_DIR, False)
    return text, 200, {
        "Content-type": "text/json; charset=utf-8"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port_number)
