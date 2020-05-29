import os
from flask import current_app, request
from flask_login import current_user
from translations import COLUMN_LABELS
from app import my_logger


def translate_column(key):
    # language = current_user.language
    # ...
    language = "DE"
    if key in COLUMN_LABELS:
        return COLUMN_LABELS[key][language]
    return "Übersetzung für Key:{0} nicht gefunden".format(key)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def get_url_for_abs_path(path):
    splitted = str(path).split("/app")
    print(splitted)
    if len(splitted) > 1:
        return splitted[1]
    return ""


def get_real_ip():
    my_logger.debug("x-real-ip: {0}".format(request.headers.getlist("X-Real-IP")))
    if request.headers.getlist("X-Real-IP"):
        ip = request.headers.getlist("X-Real-IP")[0]
    else:
        ip = request.remote_addr
    return ip
