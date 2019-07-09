/**
 * Created by veblen on 2017/3/24.
 */

$(function () {
    $("#btn-graph-captcha").click(function (event) {
        event.preventDefault();

        var imgTag = $(this).children('img');
        var oldSrc = imgTag.attr('src');
        var href = xtparam.setParam(oldSrc, 'xx', Math.random());
        // var newSrc = oldSrc + '?img='+ Math.random();
        imgTag.attr('src', href);

    });
});
