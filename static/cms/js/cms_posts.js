/**
 * Created by veblen on 2017/4/5.
 */

//加精事件
$(function () {
    $('.btn-highlight').click(function (event) {
        event.preventDefault();

        var post_id = $(this).attr('data-post-id');
        var is_highlight = parseInt($(this).attr('data-is-highlight'));

        xtajax.post({
            'url': '/posts/highlight/',
            'data': {
                'post_id': post_id,
                'is_highlight': !is_highlight
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    var msg = '';
                    if (is_highlight) {
                        msg = '取消加精成功';
                    } else {
                        msg = '加精成功';
                    }
                    xtalert.alertSuccessToast(msg);
                    setTimeout(function () {
                        window.location.reload()
                    }, 500);
                } else {
                    xtalert.alertInfoToast(data['message'])
                }
            }

        })

    });
});

// 移除事件
$(function () {
    $(".btn-removed").click(function (event) {
        event.preventDefault();

        post_id = $(this).attr("data-post-id");

        xtajax.post({
            'url' :'/posts/removed_post/',
            'data' : {
                'post_id' : post_id
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    xtalert.alertSuccessToast('帖子移除成功');
                    setTimeout(function () {
                        window.location.reload()
                    }, 500);
                } else {
                    xtalert.alertInfoToast(data['message'])
                }
            }
        })


    });
});

//排序
$(function(){
    $("#sort-select").change(function (event) {
        event.preventDefault();
        var value = $(this).val();
        window.location = xtparam.setParam(window.location.href,'sort',value);
    })
});

//板块过滤
$(function(){
    $("#board-filter-select").change(function (event) {
        event.preventDefault();
        var value = $(this).val();
        window.location = xtparam.setParam(window.location.href,'board',value);
    })
});
