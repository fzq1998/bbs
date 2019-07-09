/**
 * Created by veblen on 2017/3/22.
 */
$(function () {
    $("#btn-submit").on('click', function (event) {
        event.preventDefault();
        var checkedInputs = $(':checkbox:checked');
        var roles = [];
        checkedInputs.each(function () {
            var role_id = $(this).val();
            roles.push(role_id)
        });

        var user_id = $(this).attr('data-user-id');
        xtajax.post({
            'url': '/all_cmsuser/edit_cms_user/',
            'data': {
                'user_id': user_id,
                'roles': roles
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    xtalert.alertSuccessToast('恭喜,CMS用户已经成功修改')
                } else {
                    xtalert.alertInfoToast(data['message'])
                }
            }
        })
    })
});


$(function () {
    $("#btn-black-list").click(function (event) {
        event.preventDefault();

        var user_id = $(this).attr('data-user-id');
        var is_active = $(this).attr('data-is-active');

        var is_black = parseInt(is_active);

        xtajax.post({
            'url': '/all_cmsuser/edit_cms_user/black_cms_user/',
            'data': {
                'user_id': user_id,
                'is_black': is_black
            },
            'success': function (data) {
                var msg = '';
                if (is_black) {
                    msg = '已将CMS用户拉入黑名单';
                } else {
                    msg = '已将CMS用户从黑名单中移出';
                }
                xtalert.alertSuccessToast(msg);
                setTimeout(function () {
                    window.location.reload();
                }, 500);
                if (data['code'] == 200) {

                } else {
                    xtalert.alertInfoToast(data['message'])
                }
            }
        })
    })
});