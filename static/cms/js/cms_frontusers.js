/**
 * Created by veblen on 2017/3/25.
 */

$(function () {
    $("#sort-select").change(function (event) {
        event.preventDefault();
        var value = $(this).val();
        window.location = xtparam.setParam(window.location.href, 'sort', value);
    })
});
