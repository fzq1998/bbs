/**
 * Created by veblen on 2017/3/25.
 */
$(function () {
    $("#btn-black-list").click(function (event) {
        event.preventDefault();

        var is_active = parseInt($(this).attr('data-is-active'));
        var user_id = $(this).attr('data-user-id');

        var is_black = is_active;
        xtajax.post({
            'url': '/all_frontuser/edit_front_user/black_front_user/',
            'data': {
                'user_id': user_id,
                'is_black': is_black
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    var msg = '';
                    if (is_black) {
                        msg = '已将前台用户禁用';
                    } else {
                        msg = '已将前台用户取消禁用'
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

    });
});