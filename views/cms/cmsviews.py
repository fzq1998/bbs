# !/usr/bin/env python
# coding: utf-8

from flask import Blueprint

bp = Blueprint('cms', __name__, subdomain='cms')

import flask
import constants
from forms.cms.cmsforms import CMSLoginForm, CMSResetpwdForm, CMSResetmailForm, CMSAdduserForm, CMSBlackCMSUserForm, \
    CMSBlackFrontUserForm, CMSEditBoardsForm, CMSHighlightPostForm
from models.cms.cmsmodels import CMSUser, CMSRole
from models.common.commonmodels import BoardModel, PostModel, HighlightPostModel, CommentModel
from models.common.modelhelpers import PostModelHelper
from models.front.frontmodels import FrontUser
from flask.views import MethodView
from decorators.cms.cmsdecorators import login_required, superadmin_required
from exts import db
from utils import xtjson, xtcache, xqmail
from utils.captcha.xtcaptcha import Captcha


@bp.route('/')
@login_required
def index():
    return flask.render_template('cms/cms_index.html')


# CMS用户登录
class CMSLoginView(MethodView):

    def get(self, message=None):
        return flask.render_template('cms/cms_login.html', message=message)

    def post(self):
        form = CMSLoginForm(flask.request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                if not user.is_active:
                    return flask.abort(401)
                flask.session[constants.CMS_SESSION_ID] = user.id
                if not remember:
                    flask.session.permanent = False
                else:
                    flask.session.permanent = True
                return flask.redirect(flask.url_for('cms.index'))
            else:
                return self.get(message=u'邮箱或密码错误')
        else:
            message = form.get_error()
            return self.get(message=message)


bp.add_url_rule('/login/', view_func=CMSLoginView.as_view('login'))


# 退出登录
@bp.route('/logout/')
def logout():
    flask.session.pop(constants.CMS_SESSION_ID)
    return flask.redirect(flask.url_for('cms.login'))


# 个人详情页
@bp.route('/profile/')
@login_required
def profile():
    return flask.render_template('cms/cms_profile.html')


# 重置密码
@bp.route('/resetpwd/', methods=['GET', 'POST'])
@login_required
def resetpwd():
    if flask.request.method == 'GET':
        return flask.render_template('cms/cms_resetpwd.html')
    else:
        form = CMSResetpwdForm(flask.request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            if flask.g.cms_user.check_password(oldpwd):
                flask.g.cms_user.password = newpwd
                if oldpwd == newpwd:
                    return xtjson.json_params_error(u'新密码与旧密码一致，请重新输入密码')
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(u'密码错误')
        else:
            message = form.get_error()
            return xtjson.json_params_error(message)


# 重置邮箱
@bp.route('/resetmail/', methods=['GET', 'POST'])
@login_required
def resetmail():
    if flask.request.method == 'GET':
        return flask.render_template('cms/cms_resetmail.html')
    else:
        form = CMSResetmailForm(flask.request.form)
        if form.validate():
            email = form.email.data
            flask.g.cms_user.email = email
            if flask.g.cms_user.email == email:
                return xtjson.json_params_error(message=u'新邮箱与当前登录邮箱一致，无需修改')
            db.session.commit()
            return xtjson.json_result()
        else:
            msg = form.get_error()
            return xtjson.json_params_error(msg)


# 发送邮箱验证码
@bp.route('/resetmail/mail_captcha/')
@login_required
def mail_captcha():
    email = flask.request.args.get('email')
    if xtcache.get(email):
        return xtjson.json_params_error(u'已经给该邮箱发送验证码,请勿重复发送!')
    captcha = Captcha.gene_text()
    if xqmail.send_mail(subject=u'论坛验证码', receivers=email, body=u'您的验证码为：' + captcha + u'，请您注意保密'):
        xtcache.set(email, captcha)
        return xtjson.json_result()
    else:
        return xtjson.json_server_error()


# 所有的CMS用户
@bp.route('/all_cmsuser/')
@login_required
@superadmin_required
def all_cmsuser():
    users = CMSUser.query.all()
    context = {
        'users': users
    }
    return flask.render_template('cms/cms_users.html', **context)


# 添加CMS用户
@bp.route('/all_cmsuser/add_cms_user/', methods=['GET', 'POST'])
@login_required
@superadmin_required
def add_cms_user():
    if flask.request.method == "GET":
        roles = CMSRole.query.all()
        context = {
            'roles': roles
        }
        return flask.render_template('cms/cms_addcmsuser.html', **context)
    else:
        form = CMSAdduserForm(flask.request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            roles = flask.request.form.getlist('roles[]')
            print roles
            if not roles:
                return xtjson.json_params_error(message=u'必须最少指定一个分组!')
            user = CMSUser(username=username, email=email, password=password)
            for role_id in roles:
                role = CMSRole.query.get(role_id)
                role.users.append(user)
            if email == CMSUser.query.filter_by(email=email).first():
                return xtjson.json_params_error(message=u'该CMS用户已经存在,请勿重复添加!')
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


# 编辑CMS用户
@bp.route('/all_cmsuser/edit_cms_user/', methods=['GET', 'POST'])
@login_required
@superadmin_required
def edit_cms_user():
    if flask.request.method == 'GET':
        user_id = flask.request.args.get('user_id')
        if not user_id:
            return flask.abort(404)
        user = CMSUser.query.get(user_id)
        roles = CMSRole.query.all()
        current_roles = [role.id for role in user.roles]
        context = {
            'user': user,
            'roles': roles,
            'current_roles': current_roles
        }
        return flask.render_template('cms/cms_editcmsuser.html', **context)
    else:
        user_id = flask.request.form.get('user_id')
        if not user_id:
            return xtjson.json_params_error(message=u'用户不存在')
        roles = flask.request.form.getlist('roles[]')
        if not roles:
            return xtjson.json_params_error(message=u'必须最少指定一个分组')
        user = CMSUser.query.get(user_id)
        user.roles[:] = []
        for role_id in roles:
            role_model = CMSRole.query.get(role_id)
            user.roles.append(role_model)
        db.session.commit()
        return xtjson.json_result()


# 拉黑CMS用户
@bp.route('/all_cmsuser/edit_cms_user/black_cms_user/', methods=['POST'])
@login_required
@superadmin_required
def black_cms_user():
    form = CMSBlackCMSUserForm(flask.request.form)
    if form.validate():
        user_id = form.user_id.data
        if user_id == flask.g.cms_user.id:
            return xtjson.json_params_error(message=u'不能拉黑自己')
        is_black = form.is_black.data
        user = CMSUser.query.get(user_id)
        user.is_active = not is_black
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


# 所有的前台用户
@bp.route('/all_frontuser/')
@login_required
def all_frontuser():
    sort = flask.request.args.get('sort')
    # 1 按加入时间排序
    # 2 按帖子数排序
    # 3 按评论数排序
    # 4 按积分排序
    frontusers = None
    if not sort or sort == '1':
        frontusers = FrontUser.query.order_by(FrontUser.join_time.desc()).all()
    elif sort == '2':
        frontusers = db.session.query(FrontUser).outerjoin(PostModel).group_by(FrontUser.id).order_by(
            db.func.count(PostModel.id).desc(), FrontUser.join_time.desc())
    elif sort == '3':
        frontusers = db.session.query(FrontUser).outerjoin(CommentModel).group_by(FrontUser.id).order_by(
            db.func.count(CommentModel.id).desc(), FrontUser.join_time.desc())
    elif sort == '4':
        frontusers = FrontUser.query.order_by(FrontUser.points.desc()).all()
    else:
        frontusers = FrontUser.query.all()

    context = {
        'frontusers': frontusers,
        'current_sort': sort
    }
    return flask.render_template('cms/cms_frontusers.html', **context)


# 编辑前台用户
@bp.route('/all_frontuser/edit_front_user/')
@login_required
def edit_front_user():
    user_id = flask.request.args.get('id')
    if not user_id:
        return flask.abort(404)

    user = FrontUser.query.get(user_id)
    if not user:
        return flask.abort(404)

    return flask.render_template('cms/cms_editfrontusers.html', current_user=user)


# 拉黑前台用户
@bp.route('/all_frontuser/edit_front_user/black_front_user/', methods=['POST'])
@login_required
def black_front_user():
    form = CMSBlackFrontUserForm(flask.request.form)
    if form.validate():
        user_id = form.user_id.data
        is_black = form.is_black.data
        user = FrontUser.query.get(user_id)
        if not user:
            return flask.abort(404)
        user.is_active = not is_black
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


# 所有的板块
@bp.route('/boards/')
@login_required
def boards():
    all_board = BoardModel.query.all()
    context = {
        'boards': all_board
    }
    return flask.render_template('cms/cms_boards.html', **context)


# 添加板块
@bp.route('/boards/add_board/', methods=['POST'])
@login_required
def add_board():
    name = flask.request.form.get('name')
    # 1 判断name参数
    if not name:
        return xtjson.json_params_error(message=u'板块不存在')
    # 2 判断这个名字是否存在
    board = BoardModel.query.filter_by(name=name).first()
    if board:
        return xtjson.json_params_error(message=u'该板块已经存在，请勿重复添加')
    # 3 创建板块模型
    board = BoardModel(name=name)
    board.author = flask.g.cms_user
    db.session.add(board)
    db.session.commit()
    return xtjson.json_result()


# 编辑板块
@bp.route('/boards/edit_board/', methods=['POST'])
def edit_board():
    form = CMSEditBoardsForm(flask.request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        board.name = name
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


# 删除板块
@bp.route('/boards/delete_board/', methods=['POST'])
def delete_board():
    board_id = flask.request.form.get('board_id')
    if not board_id:
        return xtjson.json_params_error(message=u'没有板块id')
    board = BoardModel.query.filter_by(id=board_id).first()
    if not board:
        return xtjson.json_params_error(message=u'没有该板块')
    # 判断板块下帖子是否大于0
    # if board.posts.count[0] > 0:
    #     return xtjson.json_params_error(message=u'该板块下有帖子，不能删除，请先删除帖子')
    db.session.delete(board)
    db.session.commit()
    return xtjson.json_result()


# 帖子列表
@bp.route('/posts/')
@login_required
def posts():
    sort_type = flask.request.args.get('sort', 1, type=int)
    board_id = flask.request.args.get('board', 0, type=int)
    page = flask.request.args.get('page', 1, type=int)
    context = PostModelHelper.post_list(page, sort_type, board_id)
    return flask.render_template('cms/cms_posts.html', **context)


# 加精帖子
@bp.route('/posts/highlight/', methods=['POST'])
def highlight():
    form = CMSHighlightPostForm(flask.request.form)
    if form.validate():
        post_id = form.post_id.data
        is_highlight = form.is_highlight.data
        post_model = PostModel.query.get(post_id)
        if is_highlight:
            if post_model.highlight:
                return xtjson.json_params_error(message=u'当前帖子已被加精')
            highlight_model = HighlightPostModel()
            post_model.highlight = highlight_model
            db.session.commit()
            return xtjson.json_result()
        else:
            if not post_model.highlight:
                return xtjson.json_params_error(message=u'当前帖子还未加精')
            db.session.delete(post_model.highlight)
            db.session.commit()
            return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


@bp.route('/posts/removed_post/', methods=['POST'])
def removed_post():
    post_id = flask.request.form.get('post_id')
    if not post_id:
        return xtjson.json_params_error(message=u'没有传入id')
    post_model = PostModel.query.get(post_id)
    post_model.is_removed = True
    db.session.commit()
    return xtjson.json_result()


@bp.context_processor
def cms_user_context_processor():
    if hasattr(flask.g, 'cms_user'):
        return {'cms_user': flask.g.cms_user}
    else:
        return {}


@bp.before_request
def cms_user_before_request():
    id = flask.session.get(constants.CMS_SESSION_ID)
    if id:
        user = CMSUser.query.get(id)
        flask.g.cms_user = user


@bp.errorhandler(404)
def page_not_found(error):
    if flask.request.is_xhr:
        return xtjson.json_params_error()
    else:
        return flask.render_template('common/404.html'), 404


@bp.errorhandler(401)
def cms_auth_forbidden(error):
    if flask.request.is_xhr:
        return xtjson.json_unauth_error()
    else:
        return flask.render_template('common/401.html'), 401
