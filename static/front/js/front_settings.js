/**
 * Created by veblen on 2017/4/9.
 */
$(function () {
    xtqiniu.setUp({
        'browse_btn': 'avatar-img',
        'success': function (up, file, info) {
            var imgTag = $('#avatar-img');
            imgTag.attr('src', file.name);
        }
    });
});

$(function () {
    $("#btn-settings").click(function (event) {
        event.preventDefault();

        var username = $('input[name=username]').val();
        var realname = $('input[name=realname]').val();
        var qq = $('input[name=qq]').val();
        var signature = $('#signature-area').val();
        var avatar = $('#avatar-img').attr('src');
        var gender = $("input[name='gender']:checked").val();
        var email = $('input[name=email]').val();
        var captcha = $('input[name=captcha]').val();


        xtajax.post({
            'url': '/account/settings/',
            'data': {
                'username': username,
                'realname': realname,
                'qq': qq,
                'signature': signature,
                'avatar': avatar,
                'gender': gender,
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    xtalert.alertSuccessToast('资料成功修改');
                    setTimeout(function () {
                        window.location.reload()
                    }, 500)
                } else {
                    xtalert.alertInfoToast(data['message']);
                }
            }
        })
    });
});

//发送短信验证
$(function () {
    $("#btn-captcha").click(function () {
        event.preventDefault();
        var email = $('input[name=email]').val();
        if (!email) {
            xtalert.alertInfoToast('请输入邮箱后，在发送')
        }
        // alert(email);
        xtajax.get({
            'url': '/account/settings/mail_captcha/',
            'data': {
                'email': email
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    xtalert.alertSuccessToast('验证码已发送,请注意查收');
                } else {
                    xtalert.alertInfoToast(data['message'])
                }
            }
        })
    })
});
