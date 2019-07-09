# !/usr/bin/env python
# coding: utf-8
import flask
import constants
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        id = flask.session.get(constants.FRONT_SESSION_ID)
        if id:
            return func(*args, **kwargs)
        else:
            flask.abort(401)

    return wrapper
