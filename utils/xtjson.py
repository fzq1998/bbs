#coding: utf8

from flask import jsonify

class HttpCode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500

def json_result(code=HttpCode.ok,message='',data={},kwargs={}):
    json_dict = {'code':code,'message':message,'data':data}

    if kwargs.keys():
        for k,v in kwargs.iteritems():
            json_dict[k] = v

    return jsonify(json_dict)

def json_params_error(message=''):
    """
        请求参数错误
    """
    return json_result(HttpCode.paramserror,message=message)

def json_unauth_error(message=''):
    """
        没有权限访问
    """
    return json_result(code=HttpCode.unauth,message=message)

def json_method_error(message=''):
    """
        请求方法错误
    """
    return json_result(code=HttpCode.methoderror,message=message)

def json_server_error(message=''):
    """
        服务器内部错误
    """
    return json_result(code=HttpCode.servererror,message=message or '服务器内部错误！')