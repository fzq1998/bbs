/**
 * Created by veblen on 2017/3/23.
 */

$(function () {
    $("#btn-send-captcha").on('click', function (event) {
        event.preventDefault();

        var telephone = $('input[name=telephone]').val();
        var self = $(this);
        //alert(telephone);
        if (!telephone) {
            xtalert.alertInfoToast("请输入手机号码");
            return
        }

        xtajax.get({
            'url': '/account/regist/sms_captcha/',
            'data': {
                'telephone': telephone
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    xtalert.alertSuccessToast("验证码已成功发送,请您注意查询");

                    var timeCount = 60;
                    self.attr('disabled', 'disabled');
                    var timer = setInterval(function () {
                        self.text(timeCount);
                        timeCount--;
                        if (timeCount <= 0) {
                            self.text("发送验证码");
                            self.removeAttr('disabled');
                            clearInterval(timer)
                        }
                    }, 1000)

                } else {
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });

    });
});

