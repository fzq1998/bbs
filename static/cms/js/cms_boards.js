/**
 * Created by veblen on 2017/3/26.
 */
$(function () {
    $("#btn-add-board").on('click', function (event) {
        event.preventDefault();

        xtalert.alertOneInput({
            'text': '请输入板块名称',
            'placeholder': '板块名称',
            'confirmCallback': function (inputValue) {
                //ajax
                xtajax.post({
                    'url': '/boards/add_board/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (data) {
                        if (data['code'] === 200) {
                            xtalert.alertSuccessToast('恭喜，'+inputValue+'板块添加成功');
                            setTimeout(function () {
                                window.location.reload()
                            }, 500)
                        } else {
                            xtalert.alertInfoToast(data['message'])
                        }
                    }
                })
            }
        });
    });
});

//编辑板块
$(function () {
    $(".btn-edit-board").click(function (event) {
        event.preventDefault();

        var board_id = $(this).attr('data-board-id');
        var board_name = $(this).attr('data-board-name');
        // console.log(board_name);

        xtalert.alertOneInput({
            'text': '请输入板块名称',
            'placeholder': board_name,
            'confirmCallback': function (inputValue) {
                //ajax
                xtajax.post({
                    'url': '/boards/edit_board/',
                    'data': {
                        'name': inputValue,
                        'board_id': board_id
                    },
                    'success': function (data) {
                        if (data['code'] === 200) {
                            xtalert.alertSuccessToast('恭喜，板块修改成功');
                            setTimeout(function () {
                                window.location.reload()
                            }, 500)
                        } else {
                            xtalert.alertInfoToast(data['message'])
                        }
                    }
                })
            }
        });
    })
});

//删除板块
$(function () {
    $(".btn-delete-board").click(function (event) {
        event.preventDefault();

        var board_id = $(this).attr('data-board-id');
        var board_name = $(this).attr('data-board-name');

        xtalert.alertConfirm({
            'msg': '您确定要删除'+board_name+'这个板块吗？',
            'confirmCallback': function () {
                //ajax
                xtajax.post({
                    'url': '/boards/delete_board/',
                    'data': {
                        'board_id': board_id
                    },
                    'success': function (data) {
                        if (data['code'] === 200) {
                            xtalert.alertSuccessToast('恭喜,板块已经成功删除');
                            setTimeout(function () {
                                window.location.reload();
                            }, 500);
                        } else {
                            xtalert.alertInfoToast(data['message']);
                        }
                    }
                });
            }
        })
    });
});


