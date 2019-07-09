# coding: utf8

import flask
from models.front.frontmodels import FrontUser
from constants import FRONT_SESSION_ID
from datetime import datetime
from exts import db
import constants


def login_front(telephone, password):
    user = FrontUser.query.filter_by(telephone=telephone).first()
    if user and user.check_password(password):
        # 设置session
        flask.session[FRONT_SESSION_ID] = user.id
        setattr(flask.g, 'front_user', user)
        # 获取上次登录的时间
        last_login_time = user.last_login_time
        now = datetime.now()
        if not last_login_time or last_login_time.day < now.day:
            # 加2个积分
            user.points += constants.LOGIN_UP_POINTS
        # 重新设置上次的登录时间
        user.last_login_time = datetime.now()
        db.session.commit()
        return user
    else:
        return None


def logout_front():
    flask.session.pop(FRONT_SESSION_ID, None)
