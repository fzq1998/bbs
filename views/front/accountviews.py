# !/usr/bin/env python
# coding: utf-8

from flask import Blueprint, views
import flask
import constants
from exts import db
import top.api

from models.common.front_auth import login_front, logout_front
from utils import xqmail
from models.front.frontmodels import SignInModel, FrontUser

try:
    from StringIO import StringIO
except:
    from io import BytesIO as StringIO
from utils.captcha.xtcaptcha import Captcha
from utils import xtcache, xtjson
import re
from forms.front.frontforms import FrontRegistForm, FrontLoginForm, FrontSettingsForm, FrontUserSignIn
from models.front.frontmodels import FrontUser
from datetime import datetime
from decorators.fornt.frontdecorators import login_required

bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/')
def index():
    return 'account index'


class RegistView(views.MethodView):

    def get(self, message=None, **kwargs):
        context = {
            'message': message,
        }
        context.update(kwargs)
        return flask.render_template('front/front_regist.html', **context)

    def post(self):
        form = FrontRegistForm(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return flask.redirect(flask.url_for('account.login'))
        else:
            telephone = flask.request.form.get('telephone')
            username = flask.request.form.get('username')
            return self.get(message=form.get_error(), telephone=telephone, username=username)


class LoginView(views.MethodView):

    def get(self, message=None, **kwargs):
        context = {
            'message': message,
        }
        context.update(kwargs)
        return flask.render_template('front/front_login.html', **context)

    def post(self):
        form = FrontLoginForm(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = login_front(telephone, password)
            tel = login_front(telephone, password)
            if not tel:
                return self.get(message=u'该用户不存在，请先注册后再行登录')
            if user:
                user.old_login_time = datetime.now()
                if user.old_login_time:
                    user.last_login_time = user.old_login_time
                db.session.commit()
                if not user.is_active:
                    return self.get(message=u'当前用户已被销，请联系管理员')
                if remember:
                    flask.session.permanent = True
                else:
                    flask.session.permanent = False
                return flask.redirect(flask.url_for('post.index'))
            else:
                return self.get(message=u'用户名或密码输入有误，请重新输入')
        else:
            telephone = flask.request.form.get('telephone')
            return self.get(message=form.get_error(), telephone=telephone)


bp.add_url_rule('/regist/', view_func=RegistView.as_view('regist'))
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))


# 个人设置页
@bp.route('/settings/', methods=['POST', 'GET'])
@login_required
def settings():
    if flask.request.method == 'GET':
        return flask.render_template('front/front_settings.html')
    else:
        form = FrontSettingsForm(flask.request.form)
        if form.validate():
            username = form.username.data
            realname = form.realname.data
            qq = form.qq.data
            avatar = form.avatar.data
            signature = form.signature.data
            gender = form.gender.data
            email = form.email.data
            captcha = form.captcha.data

            user_model = flask.g.front_user
            user_model.username = username
            if realname:
                user_model.realname = realname
            else:
                user_model.realname = ''
            if qq:
                user_model.qq = qq
            else:
                user_model.qq = ''
            if avatar:
                user_model.avatar = avatar
            if signature:
                user_model.signature = signature
            else:
                user_model.signature = ''
                # return  xtjson.json_params_error(message=u'个性签名不能为空')
            if gender:
                user_model.gender = gender
            if email:
                user_model.email = email
                captcha_cache = xtcache.get(email)
                if not captcha_cache or captcha_cache.lower() != captcha.lower():
                    return xtjson.json_params_error(message=u'验证码输入有误,请重新输入')
            else:
                user_model.email = ''
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


# 发送邮箱验证码
@bp.route('/settings/mail_captcha/')
def mail_captcha():
    email = flask.request.args.get('email')
    user = FrontUser.query.filter_by(email=email).first()
    if user:
        return xtjson.json_params_error(u'该邮箱已使用，请您更换邮箱')
    if xtcache.get(email):
        return xtjson.json_params_error(u'已经给该邮箱发送验证码,请勿重复发送!')
    captcha = Captcha.gene_text()
    if xqmail.send_mail(subject=u'论坛验证码', receivers=email, body=u'您的验证码为：' + captcha + u'，请您注意保密'):
        xtcache.set(email, captcha)
        return xtjson.json_result()
    else:
        return xtjson.json_server_error()


# 用户详情页
@bp.route('/profile/<user_id>', methods=['GET'])
@login_required
def profile(user_id=0):
    if not user_id:
        return flask.abort(404)

    user = FrontUser.query.get(user_id)
    if user:
        context = {
            'current_user': user
        }
        return flask.render_template('front/front_profile.html', **context)
    else:
        return flask.abort(404)


@bp.route('/profile/posts/', methods=['GET'])
@login_required
def profile_posts():
    user_id = flask.request.args.get('user_id')
    if not user_id:
        return flask.abort(404)

    user = FrontUser.query.get(user_id)
    if user:
        context = {
            'current_user': user
        }
        return flask.render_template('front/front_profile_posts.html', **context)
    else:
        return flask.abort(404)


# 签到功能
@bp.route('/sign_in/', methods=['POST'])
@login_required
def sign_in():
    form = FrontUserSignIn(flask.request.form)
    if form.validate():
        user_id = form.user_id.data
        is_sign_in = form.is_sign_in.data
        user = FrontUser.query.get(user_id)

        if user_id:
            sign_in_model = SignInModel(user_id=user_id)
            db.session.add(sign_in_model)
            user.is_sign_in = not is_sign_in
        db.session.commit()
        # signinModel = SignInModel.query.filter(SignInModel.create_time == datetime.now().day).first()
        # if signinModel:
        #     print '已签到'
        # else:
        #     print '今天没有签到'
        return xtjson.json_result()

    else:
        return xtjson.json_params_error(message=form.get_error())


# 注册时发送短信验证码
@bp.route('/regist/sms_captcha/')
def sms_captcha():
    telephone = flask.request.args.get('telephone')
    if not telephone:
        return xtjson.json_params_error(message=u'手机号不能为空！')
    p2 = re.compile('^0\d{2,3}\d{7,8}$|^1[3587]\d{9}$|^147\d{8}')
    phonematch = p2.match(telephone)
    if not phonematch:
        return xtjson.json_params_error(message=u'手机号格式错误')
    tel = FrontUser.query.filter_by(telephone=telephone).first()
    if tel:
        return xtjson.json_params_error(message=u'该手机号已被注册，请勿重复注册')
    if xtcache.get(telephone):
        return xtjson.json_params_error(message=u'验证码已发送,请于1分钟后重新发送')
    app_key = constants.ALIDAYU_APP_KEY
    app_secret = constants.ALIDAYU_APP_SECRET
    req = top.setDefaultAppInfo(app_key, app_secret)
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.extend = ""
    req.sms_type = 'normal'
    req.sms_free_sign_name = constants.ALIDAYU_SIGN_NAME
    # 给模版的参数
    captcha = Captcha.gene_text()
    req.sms_param = "{code:'%s'}" % captcha
    req.rec_num = telephone.decode('utf-8').encode('ascii')
    req.sms_template_code = constants.ALIDAYU_TEMPLATE_CODE
    try:
        resp = req.getResponse()
        xtcache.set(telephone, captcha)
        return xtjson.json_result()
    except Exception, e:
        print e
        return xtjson.json_server_error()


# 生成图形验证码
@bp.route('/graph_captcha/')
def graph_captcha():
    text, image = Captcha.gene_code()
    # StringIO 相当于一个管道
    out = StringIO()
    # 把image塞到StringIO这个管道中
    image.save(out, 'png')
    # 将StringIO的指针指向开始的地方 0
    out.seek(0)

    # 创建一个response响应对象， out.read是把图形读出来
    response = flask.make_response(out.read())
    # 指定响应的类型
    response.content_type = 'image/png'
    xtcache.set(text.lower(), text.lower(), timeout=3 * 60)
    return response


# 退出登录
@bp.route('/logout/')
def logout():
    logout_front()
    return flask.redirect(flask.url_for('post.index'))
