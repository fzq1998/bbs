/**
 * Created by veblen on 2017/3/19.
 */

$(function () {
   $("#btn-captcha").on('click',function (event) {
       event.preventDefault();
       var email = $('input[name=email]').val();

       xtajax.get({
           'url' : '/resetmail/mail_captcha/',
           'data': {
               'email' : email
           },
           'success' : function (data) {
               if(data['code'] === 200){
                   xtalert.alertSuccessToast('验证码已发送,请注意查收')
               }else{
                   xtalert.alertInfoToast(data['message'])
               }
           }
       })

   })
});

$(function () {
   $("#btn-submit").on('click',function (event) {
       event.preventDefault();

       var emailInput = $('input[name=email]');
       var captchaInput = $('input[name=captcha]');

       var email = emailInput.val();
       var captcha = captchaInput.val();

       xtajax.post({
           'url' : '/resetmail/',
           'data': {
               'email' : email,
               'captcha' : captcha
           },
           'success' : function (data) {
               if (data['code'] === 200){
                   emailInput.val('');
                   captchaInput.val('');
                   xtalert.alertSuccessToast('恭喜邮箱修改成功！');
               }else {
                   xtalert.alertInfoToast(data['message'])
               }
           }
       })


   })
});
