/**
 * Created by veblen on 2017/4/7.
 * 包括编辑器的初始化和七牛服务
 */

// 初始化编辑器
$(function () {
    var editor = new wangEditor('editor');
    editor.create();
    window.editor = editor
});

//七牛初始化
$(function () {
    var progressBox = $("#progress-box");
    var progressBar = progressBox.children(0);
    var uploadBtn = $("#btn-upload");
    xtqiniu.setUp({
        'browse_btn': 'btn-upload',
        'success': function (up, file, info) {
            var fileUrl = file.name;
            if (file.type.indexOf('video') >= 0) {
                // 视频(video)
                var videoTag = "<video width='520' height='380' controls='controls' autoplay='autoplay'><source src=" + fileUrl + ">您的浏览器不支持 video 标签,请您更换浏览器</video>";
                window.editor.$txt.append(videoTag);
            } else if (file.type.indexOf('audio') >= 0) {
                // 音频(audio)
                var AudioTag = "<audio src=" + fileUrl + " autoplay='autoplay' loop='loop' controls='controls'>您的浏览器不支持 audio 标签,请更好标签</audio>";
                window.editor.$txt.append(AudioTag);
            } else {
                // 图片(img)
                var imgTag = "<img src=" + fileUrl + " class='img-responsive'>";
                window.editor.$txt.append(imgTag);
            }
        },
        'progress': function (up, file) {//进度条事件
            var percent = file.percent;
            progressBar.attr('aria-valuenow', percent);
            progressBar.css('width', percent + '%');
            progressBar.text(percent + '%');
        },
        'fileadded': function (up, files) {
            progressBox.show();
            uploadBtn.button('loading');

        },
        'complete': function () {
            progressBox.hide();
            progressBar.attr('aria-valuenow', 0);
            progressBar.css('width', '0%');
            progressBar.text('0%');
            uploadBtn.button('reset');
        }
    });
});


