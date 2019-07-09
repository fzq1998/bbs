# coding: utf8

from flask import jsonify


class HttpCode(object):
    ok = 200
    params_error = 400
    un_auth = 401
    method_error = 405
    server_error = 500


def json_result(code=HttpCode.ok, message='', data={}, kwargs={}):
    json_dict = {'code': code, 'message': message, 'data': data}

    if kwargs.keys():
        for k, v in kwargs.iteritems():
            json_dict[k] = v

    return jsonify(json_dict)


def json_params_error(message=''):
    """
        请求参数错误
    """
    return json_result(HttpCode.params_error, message=message)


def json_un_auth_error(message=''):
    """
        没有权限访问
    """
    return json_result(code=HttpCode.un_auth, message=message)


def json_method_error(message=''):
    """
        请求方法错误
    """
    return json_result(code=HttpCode.method_error, message=message)


def json_server_error(message=''):
    """
        服务器内部错误
    """
    return json_result(code=HttpCode.server_error, message=message or '服务器内部错误！')
