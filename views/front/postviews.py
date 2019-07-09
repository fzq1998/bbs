#!/usr/bin/env python
# coding: utf-8

from flask import Blueprint
import flask
import constants
from models.front.frontmodels import FrontUser, SignInModel
from models.common.commonmodels import BoardModel, PostModel, CommentModel, PostStarModel
from models.common.modelhelpers import PostModelHelper
from utils import xtjson
from exts import db
from decorators.fornt.frontdecorators import login_required
from forms.front.frontforms import FrontSendPostForm, FrontAddCommentForm, FrontPostStarForm
import qiniu

bp = Blueprint('post', __name__)


@bp.route('/')
def index():
    return post_list(1, 1, 0)


@bp.route('/list/<int:page>/<int:sort_type>/<int:board_id>')
def post_list(page, sort_type, board_id):
    context = PostModelHelper.post_list(page, sort_type, board_id)
    return flask.render_template('front/front_index.html', **context)


@bp.route('/add_post/', methods=['GET', 'POST'])
@login_required
def add_post():
    if flask.request.method == 'GET':
        boards = BoardModel.query.all()
        context = {
            'boards': boards
        }
        return flask.render_template('front/front_addpost.html', **context)
    else:
        form = FrontSendPostForm(flask.request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            post_model = PostModel(title=title, content=content)
            board_model = BoardModel.query.filter_by(id=board_id).first()
            if not board_model:
                return xtjson.json_params_error(message=u'不存在该板块')
            post_model.board = board_model
            post_model.author = flask.g.front_user
            db.session.add(post_model)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


@bp.route('/post/detail/<int:post_id>')
def post_detail(post_id):
    post_model = PostModel.query.filter(PostModel.is_removed == False, PostModel.id == post_id).first()
    if not post_model:
        return flask.abort(404)
    star_author_ids = [star_model.author.id for star_model in post_model.stars]
    # 以下可以简写成 star_model.author.id for star_model in post_model.stars
    # for star_model in post_model.stars:
    #     star_author_ids.append(star_model.author.id)
    post_model.read_count += 1
    db.session.commit()

    context = {
        'post': post_model,
        'star_author_ids': star_author_ids
    }
    return flask.render_template('front/front_postdetail.html', **context)


@bp.route('/post/add_comment/', methods=['GET', 'POST'])
@login_required
def post_addcomment():
    if flask.request.method == 'GET':
        post_id = flask.request.args.get('post_id', type=int)
        comment_id = flask.request.args.get('comment_id', type=int)
        context = {
            'post': PostModel.query.get(post_id)
        }
        if comment_id:
            context['origin_comment'] = CommentModel.query.get(comment_id)
        return flask.render_template('front/front_addcomment.html', **context)
    else:
        form = FrontAddCommentForm(flask.request.form)
        if form.validate():
            # 先判断该用户是否满足COMMENT_ALLOW_POINTS个积分
            if flask.g.front_user.points < constants.COMMENT_ALLOW_POINTS:
                message = u'您必须达到%s个积分才能评论！' % constants.COMMENT_ALLOW_POINTS
                return xtjson.json_params_error(message=message)
            post_id = form.post_id.data
            content = form.content.data
            comment_id = form.comment_id.data

            comment_model = CommentModel(content=content)
            comment_model.author = flask.g.front_user
            post_model = PostModel.query.get(post_id)
            comment_model.post = post_model
            if comment_id:
                origin_comment = CommentModel.query.get(comment_id)
                comment_model.origin_comment = origin_comment
            # 评论一次加comment_up_points个积分
            flask.g.front_user.points += constants.COMMENT_UP_POINTS
            db.session.add(comment_model)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())


@bp.route('/post/star/', methods=['POST'])
@login_required
def post_star():
    form = FrontPostStarForm(flask.request.form)
    if form.validate():
        post_id = form.post_id.data
        is_star = form.is_star.data
        post_model = PostModel.query.get(post_id)
        star_model = PostStarModel.query.filter_by(author_id=flask.g.front_user.id, post_id=post_id).first()
        if is_star:
            if star_model:
                return xtjson.json_params_error(message=u'已点赞，无需再赞')
            star_model = PostStarModel()
            star_model.author = flask.g.front_user
            star_model.post = post_model
            # 点赞一次加star_up_points个积分
            flask.g.front_user.points += constants.STAR_UP_POINTS
            db.session.add(star_model)
            db.session.commit()
            return xtjson.json_result()
        else:
            if star_model:
                # 取消点赞一次扣除star_up_points个积分
                flask.g.front_user.points -= constants.STAR_UP_POINTS
                db.session.delete(star_model)
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(message=u'你尚未点赞')
    else:
        return xtjson.json_params_error(message=form.get_error())


@bp.route('/test/')
def test():
    # author = FrontUser.query.first()
    # board = BoardModel.query.first()
    # for x in xrange(0,100):
    #     title = '帖子标题 %s' % x
    #     content = '帖子内容 %s' % x
    #     post_model = PostModel(title=title,content=content)
    #     post_model.author = author
    #     post_model.board = board
    #     db.session.add(post_model)
    # db.session.commit()
    # return 'success'
    pass


@bp.route('/qiniu_token/')
def qiniu_token():
    # 授权
    q = qiniu.Auth(constants.QINIU_ACCESS_KEY, constants.QINIU_SECRET_KEY)
    # 选择七牛的云空间
    bucket_name = 'fubbs'
    # 生成token
    token = q.upload_token(bucket_name)
    return flask.jsonify({'uptoken': token})
