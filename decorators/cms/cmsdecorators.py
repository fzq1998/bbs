# !/usr/bin/env python
# coding: utf-8
import flask
import constants
from functools import wraps
from models.cms.cmsmodels import CMSPermission


# cms登录权限
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        id = flask.session.get(constants.CMS_SESSION_ID)
        if id:
            return func(*args, **kwargs)
        else:
            return flask.redirect(flask.url_for('cms.login'))

    return wrapper


# Authority
def permission_required(permission):
    def auth(func):
        @wraps(func)
        def warpper(*args, **kwargs):
            if flask.g.cms_user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                flask.abort(401)

        return warpper

    return auth


# superadmin
def superadmin_required(func):
    return permission_required(CMSPermission.ADMINSTRATOR)(func)
