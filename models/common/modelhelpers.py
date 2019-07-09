# !/usr/bin/env python
# coding: utf-8

# 这是文件专门用来给模型添加方法

from models.common.commonmodels import PostModel, HighlightPostModel, CommentModel, PostStarModel, BoardModel
from exts import db
import constants


class PostModelHelper(object):
    class PostSortType(object):
        CREATE_TIME = 1  # 1 按发表时间排序
        HIGHLIGHT_TIME = 2  # 2 按加精帖子排序
        STAR_COUNT = 3  # 3 按点赞数量排序
        COMMENT_COUNT = 4  # 4 按评论数量排序

    @classmethod
    def post_list(cls, page, sort_type, board_id):
        posts = None
        if sort_type == cls.PostSortType.CREATE_TIME:
            posts = PostModel.query.order_by(PostModel.create_time.desc())
        elif sort_type == cls.PostSortType.HIGHLIGHT_TIME:
            posts = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(
                HighlightPostModel.create_time.desc(), PostModel.create_time.desc())
        elif sort_type == cls.PostSortType.STAR_COUNT:
            posts = db.session.query(PostModel).outerjoin(PostStarModel).group_by(PostModel.id).order_by(
                db.func.count(PostStarModel.id).desc(), PostModel.create_time.desc())
        elif sort_type == cls.PostSortType.COMMENT_COUNT:
            posts = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
                db.func.count(CommentModel.id).desc(), PostModel.create_time.desc())
        else:
            posts = PostModel.query.order_by(PostModel.create_time.desc())

        posts = posts.filter(PostModel.is_removed == False)

        if board_id != 0:
            posts = posts.filter(PostModel.board_id == board_id)

        start = (page - 1) * constants.PAGE_NUM
        end = start + constants.PAGE_NUM
        boards = BoardModel.query.all()
        total_post_count = posts.count()
        total_page = total_post_count / constants.PAGE_NUM
        if total_post_count > 0:
            if total_page % total_post_count >= 0:
                total_page += 1

        pages = []

        # 往前找，前提当前页面必须大于等于1
        tmp_page = page - 1
        while tmp_page >= 1:
            if tmp_page % 5 == 0:
                break
            else:
                pages.append(tmp_page)
                tmp_page -= 1

        # 往后找，前提是当前页面不能大于总页面
        tmp_page = page
        while tmp_page <= total_page:
            if tmp_page % 5 == 0:
                pages.append(tmp_page)
                break
            else:
                pages.append(tmp_page)
                tmp_page += 1
        pages.sort()

        context = {
            'boards': boards,
            'posts': posts.slice(start, end),
            'pages': pages,
            'c_page': page,
            't_page': total_page,
            'c_sort': sort_type,
            'c_board': board_id,
        }
        return context
