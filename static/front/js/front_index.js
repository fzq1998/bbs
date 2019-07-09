/**
 * Created by veblen on 2017/4/14.
 */
//签到
$(function () {
    $("#btn-sign-in").click(function (event) {
        event.preventDefault();

        var user_id = $(this).attr('data-user-id');
        //alert(user_id)
        var is_sign_in = parseInt($(this).attr('data-is-sign-in'));
        xtajax.post({
            'url': '/account/sign_in/',
            'data': {
                'user_id': user_id,
                'is_sign_in': is_sign_in
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    xtalert.alertSuccessToast('签到成功！');

                    setTimeout(function () {
                        window.location.reload()
                    }, 500)
                } else {
                    xtalert.alertInfoToast(data['message'])
                }
            }
        })

    });
});
