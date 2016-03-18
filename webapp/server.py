#!/usr/bin/env python

from flask import Flask
import sys
import os
import logging
import logging.config
import yaml
from langmodel import generate

port_number = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TEXT_TEMPLATE_DIR = os.path.join(SCRIPT_DIR, "..", "build", "text_template")
STATIC_DIR = os.path.join(SCRIPT_DIR, "static")


with open(os.path.join(SCRIPT_DIR, "logging.yaml")) as yaml_stream:
    log_config = yaml.load(yaml_stream)
logging.config.dictConfig(log_config)

app = Flask("lorumipse", static_folder=STATIC_DIR)

generate.init(TEXT_TEMPLATE_DIR)


@app.route("/")
def root():
    return app.send_static_file("index.html")


@app.route("/generate/init/")
def generate_first_paragraph():
    text = generate.generate_text(True)
    return text, 200, {
        "Content-type": "text/json; charset=utf-8"
    }


@app.route("/generate/")
def generate_subsequent_paragraph():
    text = generate.generate_text(False)
    return text, 200, {
        "Content-type": "text/json; charset=utf-8"
    }


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=port_number)
