/**
 * Created by veblen on 2017/4/09.
 */
$(function () {
    //点击回到顶部
    $(".f_btn").click(function () {
        $("html,body").animate({
            scrollTop: 0
        }, 1000);
    });
    //开始淡出淡入
    $(window).scroll(function () {
        //当滚动条距离顶部200px的时候开始
        if ($(window).scrollTop() >= 200) {
            $("#fu_scorll_top").fadeIn(1000);//开始淡入
        } else {
            $("#fu_scorll_top").stop(true, true).fadeOut(1000);//开始淡出
        }
    });
});