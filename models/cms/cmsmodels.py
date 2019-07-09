# !/usr/bin/env python
# coding: utf-8
from exts import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSPermission(object):
    ADMINSTRATOR = 255
    OPEATOR = 1
    PERMISSION_MAP = {
        ADMINSTRATOR: (u'超级管理员权限', u'拥有至高无上的权限'),
        OPEATOR: (u'普通管理员权限', u'可以操作帖子等相关权限')
    }


# 创建多对多关系表，关系表要在关系表前面
cms_user_role = db.Table('cms_user_role',
                         db.Column('role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
                         db.Column('user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True))


# 创建CMS组
class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(100), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    permissions = db.Column(db.Integer, nullable=False)


class CMSUser(db.Model):
    __tablename__ = 'cms_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(255), nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    join_time = db.Column(db.DateTime(), default=datetime.datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    last_login_time = db.Column(db.DateTime, nullable=True)
    roles = db.relationship('CMSRole', secondary=cms_user_role, backref='users')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, rawpwd):
        self._password = generate_password_hash(rawpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self.password, rawpwd)

    @property
    def is_superadmin(self):
        return self.has_permission(CMSPermission.ADMINSTRATOR)

    def has_permission(self, permission):
        if not self.roles:
            return None
        all_permission = 0
        for role in self.roles:
            all_permission |= role.permissions
        return all_permission & permission == permission

    @property
    def permissions(self):
        if not self.roles:
            return None
        all_permission = 0
        for role in self.roles:
            all_permission |= role.permissions

        permission_dicts = []
        for permission, permission_info in CMSPermission.PERMISSION_MAP.iteritems():
            if permission & all_permission == permission:
                permission_dicts.append({permission: permission_info})

        return permission_dicts
