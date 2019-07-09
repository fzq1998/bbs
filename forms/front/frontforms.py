# !/usr/bin/env python
# coding: utf-8

from forms.common.baseforms import BaseForm
from wtforms import StringField, BooleanField, ValidationError, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, URL, Email
from utils import xtcache


class GraphCaptchaForm(BaseForm):
    graph_captcha = StringField(validators=[InputRequired(message=u'请输入图形验证码')])

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        cache_captcha = xtcache.get(graph_captcha)
        if not cache_captcha or cache_captcha.lower() != graph_captcha.lower():
            raise ValidationError(message=u'图形验证码输入有误')
        return True


class FrontRegistForm(GraphCaptchaForm):
    telephone = StringField(validators=[InputRequired(message=u'手机号不能为空'), Length(11, 11, message=u'手机号长度错误')])
    sms_captcha = StringField(validators=[InputRequired(message=u'短信验证码不能为空'), Length(4, 4, message=u'短信验证码长度为4位')])
    username = StringField(validators=[InputRequired(message=u'用户名必须输入'), Length(3, 20, message=u'用户名长度应在3~20之间')])
    password = StringField(validators=[InputRequired(message=u'必须输入密码'), Length(6, 20, message=u'密码长度在6~20之间')])
    password_repeat = StringField(validators=[EqualTo('password', message=u'两次密码输入不一致，请重新输入')])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data
        cache_captcha = xtcache.get(telephone)
        if not cache_captcha or cache_captcha.lower() != sms_captcha.lower():
            raise ValidationError(message=u'短信验证码错误')
        return True


class FrontLoginForm(GraphCaptchaForm):
    telephone = StringField(validators=[InputRequired(message=u'用户名不能为空'), Length(11, 11, message=u'手机号长度输入有误')])
    password = StringField(validators=[InputRequired(message=u'密码不能为空'), Length(6, 20, message=u'密码长度应在6~20之间')])
    remember = BooleanField()


class FrontSendPostForm(GraphCaptchaForm):
    title = StringField(validators=[InputRequired(message=u'必须输入标题'), Length(1, 100, message=u'帖子标题应在100字以内')])
    content = StringField(validators=[InputRequired(message=u'内容不能位空')])
    board_id = IntegerField(validators=[InputRequired(message=u'必须传入id')])


class FrontAddCommentForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'帖子id不能为空')])
    content = StringField(validators=[InputRequired(message=u'内容不能位空')])
    comment_id = IntegerField()


class FrontPostStarForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message=u'帖子id不能为空')])
    is_star = BooleanField(validators=[InputRequired(message=u'必须赞或取消赞')])


class FrontSettingsForm(BaseForm):
    username = StringField(validators=[InputRequired(message=u'用户名不能为空')])
    realname = StringField()
    qq = StringField()
    avatar = StringField(validators=[URL(message=u'头像的格式不对')])
    signature = StringField()
    gender = IntegerField()
    email = StringField()
    captcha = StringField()


class FrontUserSignIn(BaseForm):
    user_id = StringField(validators=[InputRequired(message=u'用户id不能为空')])
    is_sign_in = IntegerField(validators=[InputRequired(message=u'已签到，不能重复签到')])
