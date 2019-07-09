# !/usr/bin/env python
# coding: utf-8

import os

SECRET_KEY = os.urandom(24)

DB_USERNAME = ''  # 数据库用户名
DB_PASSWORD = ''  # 数据库密码
DB_HOST = ''  # 主机地址
DB_PORT = ''  # 端口号
DB_NAME = ''  # 数据库名字

DB_UEI = "mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
SQLALCHEMY_DATABASE_URI = DB_UEI

SQLALCHEMY_TRACK_MODIFICATIONS = False

# 通过修改本地 host 文件
# SERVER_NAME = 'fzq.com:5000'

# 邮箱配置
MAIL_SERVER = ''
MAIL_PORT = ''
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = 'mrfu1998@gmail.com'
MAIL_USE_SSL = True

# QQ邮箱
# MAIL_USE_SSL:端口号465
# MAIL_USE_TLS:端口号587
