# !/usr/bin/env python
# coding: utf-8

from wtforms import StringField, BooleanField, ValidationError, IntegerField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from forms.common.baseforms import BaseForm
from utils import xtcache
from models.common.commonmodels import BoardModel


class CMSLoginForm(BaseForm):
    email = StringField(validators=[InputRequired(message=u'邮箱不能为空'), Email(message=u'邮箱输入有误')])
    password = StringField(validators=[InputRequired(message=u'密码不能为空'), Length(6, 20, message=u'密码长度应在6~20位之间')])
    remember = BooleanField()


class CMSResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[InputRequired(message=u'请输入原密码')])
    newpwd = StringField(validators=[InputRequired(message=u'请输入新密码'), Length(6, 20, message=u'新密码长度应在6~20之间')])
    newpwd_repeat = StringField(validators=[EqualTo('newpwd', message=u'两次密码不一致,请重新输入')])


class CMSResetmailForm(BaseForm):
    email = StringField(validators=[InputRequired(message=u'必须输入邮箱'), Email(message=u'您输入的邮箱格式不正确')])
    captcha = StringField(validators=[InputRequired(message=u'必须输入验证码'), Length(4, 4, message=u'验证码长度应为4位')])

    def validate_captcha(self, field):
        email = self.email.data
        captcha = field.data
        captcha_cache = xtcache.get(email)
        if not captcha_cache or captcha_cache.lower() != captcha.lower():
            raise ValidationError(message=u'验证码输入有误,请重新输入')
        return True


class CMSAdduserForm(BaseForm):
    username = StringField(validators=[InputRequired(message=u'用户名不能为空'), Length(2, 20, message=u'用户名长度应在3~20之间')])
    email = StringField(validators=[InputRequired(message=u'邮箱不能为空'), Email(message=u'邮箱格式不正确')])
    password = StringField(validators=[InputRequired(message=u'密码不能为空'), Length(6, 20, message=u'密码长度应在6~20之间')])


class CMSBlackCMSUserForm(BaseForm):
    user_id = IntegerField(validators=[InputRequired(message=u'用户id不能为空')])
    is_black = IntegerField(validators=[InputRequired(message=u'不能为空')])


class CMSBlackFrontUserForm(BaseForm):
    user_id = StringField(validators=[InputRequired(message=u'用户id不能为空')])
    is_black = IntegerField(validators=[InputRequired(message=u'不能为空')])


class CMSEditBoardsForm(BaseForm):
    board_id = IntegerField(validators=[InputRequired(message=u'板块id不能为空')])
    name = StringField(validators=[InputRequired(message=u'板块名称不能为空'), Length(3, 10, message=u'板块名称长度应在3~10位之间')])

    def validate_board_id(self, field):
        board_id = field.data
        board = BoardModel.query.filter_by(id=board_id).first()
        if not board:
            raise ValidationError(message=u'该板块不存在，不能编辑')
        return True

    def validate_board_name(self, field):
        name = field.data
        board = BoardModel.query.filter_by(name=name).first()
        if board:
            raise ValidationError(message=u'修改后的板块名称与修改前相同，请重新输入')
        return True


class CMSHighlightPostForm(BaseForm):
    post_id = StringField(validators=[InputRequired(message=u'必须传入帖子id')])
    is_highlight = BooleanField(validators=[InputRequired(message=u'必须操作事件')])
