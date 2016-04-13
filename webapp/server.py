#!/usr/bin/env python

from flask import Flask, request
import sys
import os
import logging
import logging.config
import yaml
from langmodel import generate


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TEXT_TEMPLATE_DIR = os.path.join(SCRIPT_DIR, "..", "build", "text_template")
STATIC_DIR = os.path.join(SCRIPT_DIR, "static")


with open(os.path.join(SCRIPT_DIR, "logging.yaml")) as yaml_stream:
    log_config = yaml.load(yaml_stream)
logging.config.dictConfig(log_config)

logger = logging.getLogger("server")

app = Flask("lorumipse", static_folder=STATIC_DIR)

generate.init(TEXT_TEMPLATE_DIR)


@app.route("/")
def root():
    log_request("index")
    return app.send_static_file("index.html")


@app.route("/generate/init/")
def generate_first_paragraph():
    log_request("generate_initial")
    text = generate.generate_text(True)
    return text, 200, {
        "Content-type": "text/json; charset=utf-8"
    }


@app.route("/generate/")
def generate_subsequent_paragraph():
    log_request("generate_other")
    text = generate.generate_text(False)
    return text, 200, {
        "Content-type": "text/json; charset=utf-8"
    }


def log_request(view):
    logger.info(" ".join(["request", view, get_remote_address()]))


def get_remote_address():
    return request.access_route[-2] if len(request.access_route) > 1 else request.access_route[0]


if __name__ == "__main__":
    port_number = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
    app.run(host="0.0.0.0", port=port_number)
