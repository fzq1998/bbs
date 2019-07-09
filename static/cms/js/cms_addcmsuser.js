/**
 * Created by veblen on 2017/3/19.
 */
$(function () {
    $("#btn-submit").on('click',function(event) {
        event.preventDefault();

        var usernameInput = $('input[name=username]');
        var emailInput = $('input[name=email]');
        var passwordInput = $('input[name=password]');
        var selectedCheckbox = $(':checkbox:checked');

        var username = usernameInput.val();
        var email = emailInput.val();
        var password = passwordInput.val();
        var roles = [];
        selectedCheckbox.each(function () {
            var role_id = $(this).val();
            roles.push(role_id);
        });

        xtajax.post({
            'url' : '/all_cmsuser/add_cms_user/',
            'data' : {
                'username' : username,
                'email' : email,
                'password' : password,
                'roles' : roles
            },
            'success': function (data) {
                if(data['code'] === 200){
                    usernameInput.val('');
                    emailInput.val('');
                    passwordInput.val('');
                    selectedCheckbox.each(function () {
                        $(this).prop('checked',false)
                    });
                    xtalert.alertSuccessToast('恭喜,CMS用户创建成功')

                }else {
                    xtalert.alertInfoToast(data['message'])
                }
            }
        })



    });
});

