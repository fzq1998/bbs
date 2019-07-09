/**
 * Created by veblen on 2017/4/7.
 */

//添加评论
$(function () {
    $("#btn-addComment").click(function (event) {
        event.preventDefault();

        var post_id = $(this).attr('data-post-id');
        var content = window.editor.$txt.html();
        var comment_id = $(".origin-comment-group").attr('data-comment-id');

        xtajax.post({
            'url': '/post/add_comment/',
            'data': {
                'post_id': post_id,
                'content': content,
                'comment_id': comment_id
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    xtalert.alertSuccessToast('评论成功!');
                    setTimeout(function () {
                        window.location = '/post/detail/' + post_id;
                    }, 500)
                } else {
                    xtalert.alertInfoToast(data['message']);
                }
            }
        })


    });
});