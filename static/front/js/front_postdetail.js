/**
 * Created by veblen on 2017/4/8.
 */

//点赞的事件
$(function () {
    $("#btn-star").click(function (event) {
        event.preventDefault();

        var post_id = $(this).attr('data-post-id');
        var is_star = parseInt($(this).attr('data-is-star'));
        var is_login = parseInt($(this).attr('data-is-login'));
        if (!is_login) {
            window.location = '/account/login/';
            return;
        }

        xtajax.post({
            'url': '/post/star/',
            'data': {
                'post_id': post_id,
                'is_star': !is_star
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    var msg = '';
                    if (is_star) {
                        msg = '取消赞成功'
                    } else {
                        msg = '点赞成功'
                    }
                    xtalert.alertSuccessToast(msg);
                    setTimeout(function () {
                        window.location.reload();
                    }, 500);
                } else {
                    xtalert.alertInfoToast(data['message'])
                }
            }
        })

    })
});