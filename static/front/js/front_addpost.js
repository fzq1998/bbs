/**
 * Created by veblen on 2017/3/26.
 */

//发布帖子按钮执行的事件
$(function () {
    $('#btn-send-post').click(function (event) {
        event.preventDefault();

        var titleInput = $('input[name=title]');
        var graphCaptchaInput = $('input[name=graph_captcha]');

        //获取标题内容
        var title = titleInput.val();
        //获取用户选择的板块
        var board_id = $('.sort-select').val();
        //获取富文本编辑器内容
        var content = window.editor.$txt.html();
        //获取验证码的内容
        var graph_captcha = graphCaptchaInput.val();

        xtajax.post({
            'url': '/add_post/',
            'data': {
                'title': title,
                'board_id': board_id,
                'content': content,
                'graph_captcha': graph_captcha
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    xtalert.alertConfirm({
                        'msg': '恭喜！帖子发表成功',
                        'cancelText': '回到首页',
                        'confirmText': '再发一篇',
                        'cancelCallback': function () {
                            window.location = '/'
                        },
                        'confirmCallback': function () {
                            titleInput.val('');
                            window.editor.clear();
                            graphCaptchaInput.val('');
                            $('#btn-graph-captcha').click();
                        }
                    })
                } else {
                    xtalert.alertInfoToast(data['message']);
                    $('#btn-graph-captcha').click();
                }
            }
        })
    });
});

