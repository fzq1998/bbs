# coding:utf-8

from flask import Flask
import flask

import constants
from exts import db, mail
import config
from models.front.frontmodels import FrontUser
from utils import xtjson
from views.front import postviews, accountviews
from views.cms import cmsviews
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.debug = True
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
CSRFProtect(app)

app.register_blueprint(postviews.bp)
app.register_blueprint(accountviews.bp)
app.register_blueprint(cmsviews.bp)


@app.context_processor
def post_context_processor():
    if hasattr(flask.g, 'front_user'):
        return {'front_user': flask.g.front_user}
    return {}


@app.before_request
def post_before_request():
    id = flask.session.get(constants.FRONT_SESSION_ID)
    if id:
        user = FrontUser.query.get(id)
        flask.g.front_user = user


@app.errorhandler(401)
def post_auth_forbidden(error):
    if flask.request.is_xhr:
        return xtjson.json_unauth_error()
    else:
        return flask.redirect(flask.url_for('account.login'))


@app.errorhandler(404)
def page_not_found(error):
    if flask.request.is_xhr:
        return xtjson.json_params_error()
    else:
        return flask.render_template('common/404.html'), 404


@app.template_filter('handle_time')
def handle_time(time):
    from datetime import datetime
    if type(time) == datetime:
        now = datetime.now()
        timestamp = (now - time).total_seconds()
        if timestamp < 60:
            return u'刚刚'
        elif timestamp > 60 and timestamp < 60 * 60:
            minutes = timestamp / 60
            return u'%s分钟前' % int(minutes)
        elif timestamp > 60 * 60 and timestamp < 60 * 60 * 24:
            hours = timestamp / (60 * 60)
            return u'%s小时前' % int(hours)
        elif timestamp > 60 * 60 * 24 and timestamp < 60 * 60 * 24 * 30:
            days = timestamp / (60 * 60 * 24)
            return u'%s天前' % int(days)
        elif now.year == time.year:
            return time.strftime('%m-%d %H:%M:%S')
        else:
            return time.strftime('%Y-%m-%d %H:%M:%S')
    return time


if __name__ == '__main__':
    app.run(port=8000)
