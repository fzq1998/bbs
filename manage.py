# !/usr/bin/env python
# coding: utf-8

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from bbs import app
from exts import db
from models.cms import cmsmodels
from models.common import commonmodels
from models.front.frontmodels import FrontUser

CMSUser = cmsmodels.CMSUser
CMSRole = cmsmodels.CMSRole
CMsPermission = cmsmodels.CMSPermission

# 创建命令管理器
manager = Manager(app)
# 绑定app到db
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server)


@manager.option('-n', '--name', dest='name')
@manager.option('-d', '--desc', dest='desc')
@manager.option('-p', '--permissions', dest='permissions')
def create_role(name, desc, permissions):
    role = CMSRole(name=name.decode('gbk').encode('utf8'), desc=desc.decode('gbk').encode('utf8'),
                   permissions=permissions)
    db.session.add(role)
    db.session.commit()
    print u'恭喜,角色创建成功'


@manager.option('-e', '--email', dest='email')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-r', '--role_name', dest='role')
def create_cms_user(email, username, password, role):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        print u'该邮箱已被注册,不能重复注册'
        return
    roleModel = CMSRole.query.filter_by(name=role.decode('gbk').encode('utf8')).first()
    if not roleModel:
        print u'用户不存在'
        return
    user = CMSUser(email=email, password=password, username=username)
    roleModel.users.append(user)
    db.session.commit()
    print u'恭喜,CMS用户添加成功'


@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username.decode('gbk').encode('utf8'), password=password)
    db.session.add(user)
    db.session.commit()
    print u'恭喜，前台用户创建成功'


if __name__ == '__main__':
    manager.run()
