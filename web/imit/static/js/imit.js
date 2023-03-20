var imit = imit || {};

/**
 * news
 */
imit.News = (function ($) {
    /**
     * Shows cover image preview after input selecting file.
     */
    this.showCoverImageCropper = function (input) {
        if (input.files && input.files[0]) {
            $('#cropper_block').show();
            $('#cover_image_block').hide();

            var reader = new FileReader();
            reader.onload = function (e) {
                var cropper = $('#cover_image_cropper');
                cropper.cropper('destroy');
                cropper.attr('src', e.target.result);
                cropper.cropper({
                    dragMode: 'move',
                    cropBoxResizable: false,
                    cropBoxMovable: false,
                    checkCrossOrigin: false,
                    checkOrientation: false,
                    //modal: false,
                    //highlight: false,
                    rotatable: false,
                    toggleDragModeOnDblclick: false,
                    minCropBoxWidth: 150,
                    minCropBoxHeight: 100,
                    //minContainerHeight: 300,
                    aspectRatio: 2 / 1
                });
            };

            reader.readAsDataURL(input.files[0]);
        }
    };

    this.applyCrop = function () {
        var cropper = $('#cover_image_cropper');
        var img_data = cropper.cropper('getCroppedCanvas',
            {width: 150, height: 100}).toDataURL("image/png");
        $('#cropped_cover_image_data').val(img_data);
        $('#cover_image_preview').attr('src', img_data);
        cropper.cropper('destroy');
        $('#cropper_block').hide();
        $('#cover_image_block').show();
        $('#delete_cover_image').prop('checked', false);
        return false;
    };

    this.cancelCrop = function () {
        $('#cover_image_cropper').cropper('destroy');
        $('#cropper_block').hide();
        if (!$('#delete_cover_image').prop('checked')) {
            $('#cover_image_block').show();
        }
        return false;
    };

    this.initTinyMCE = function (selector, title) {
        tinymce.init({
            selector: selector,
            fontsize_formats: '8pt 10pt 12pt 14pt 18pt 24pt 36pt',
            plugins: ['advlist autolink lists link image media charmap preview anchor',
                'searchreplace visualblocks code fullscreen textcolor colorpicker',
                'insertdatetime table contextmenu paste code print spellchecker imagetools '],
            toolbar1: 'insertfile undo redo | styleselect | fontsizeselect | bold italic underline strikethrough | ' +
            'forecolor backcolor | alignleft aligncenter alignright alignjustify | ' +
            'bullist numlist outdent indent',
            toolbar2: 'subscript superscript | link anchor image | charmap | print preview | spellchecker',
            language: 'ru',
            image_advtab: true,
            spellchecker_languages: "Russian=ru,English=en",
            spellchecker_language: "ru",  // default language
            spellchecker_rpc_url: "http://speller.yandex.net/services/tinyspell",
            title: title,
            height: "400",
            language_url: '/js/tinymce_ru.js',
            relative_urls: false,
            remove_script_host: false,
            convert_urls: true,
        });
    };

    $(function () {
        $("#full_cover_image").change(function () {
            imit.News.showCoverImageCropper(this);
        });
        $("#apply_crop_button").click(imit.News.applyCrop);
        $("#cancel_crop_button").click(imit.News.cancelCrop);

        $("#delete_cover_image_button").click(function () {
            $('#cropper_block').hide();
            $('#cover_image_block').hide();
            $('#delete_cover_image').prop('checked', true);
            $('#full_cover_image').val(null);
            return false;
        });
    });

    return this;
}).call(imit.News || {}, jQuery);

imit.FileManager = (function ($) {
    this.chooseFile = function (event) {
        var fli = $(this);
        var fid = fli.attr("fid");
        var fmef = $("#fm_edit_form");
        var fmrf = $("#fm_remove_form");
        var cflb = $('#fm_copy_link_button');
        var iflb = $('#fm_insert_link_button');

        if (window.fm_options.chosen_file == fid) {
            window.fm_options.chosen_file = null;
            fli.removeClass("chosen_file");
            fmef.hide();
            fmrf.hide();
            cflb.hide();
            iflb.hide();
        } else {
            if (window.fm_options.chosen_file != null && window.fm_options.chosen_file != undefined) {
                $("#fm_list").find("li[fid=" + window.fm_options.chosen_file + "]").removeClass("chosen_file");
            }
            window.fm_options.chosen_file = fli.attr("fid");
            fli.addClass("chosen_file");
            fmef.find("#description").val(fli.text());
            fmef.find("#file_id").val(fli.attr("fid"));
            fmef.show();
            fmrf.find("#file_id").val(fli.attr("fid"));
            fmrf.show();
            cflb.show();
            iflb.show();
        }
    };

    this.initFileManager = function (options) {
        window.fm_options = {
            target: null, target_id: null,
            block: false,
            block_message: null,
            chosen_file: null
        };
        if (options.page) {
            window.fm_options.target = "page";
            window.fm_options.target_id = options.page;
            $("#fm_add_form").find("#page_id").val(options.page);
        } else {
            if (options.post) {
                window.fm_options.target = "post";
                window.fm_options.target_id = options.post;
                $("#fm_add_form").find("#post_id").val(options.post);
            }
        }
        window.fm_options.block = options.block;
        window.fm_options.block_message = options.block_message;
        if (window.fm_options.block) {
            $("#fm_add_form").remove();
            $("#fm_edit_form").remove();
            $("#fm_delete_form").remove();
            $("#fm_title").append(" " + window.fm_options.block_message);
        } else {
            imit.FileManager.updateFileManager();
        }
        new Clipboard('#fm_copy_link_button');
    };

    this.updateFileManager = function () {
        var ul = $("#fm").find("#fm_list");
        var url = "/fm/list";
        if (window.fm_options.target) {
            url += "/" + window.fm_options.target + "/" + window.fm_options.target_id;
        }
        $.getJSON($SCRIPT_ROOT + url, {},
            function (data) {
                ul.empty();
                for (var i = 0; i < data.length; i++) {
                    var li = $("<li class='fm_list_item'></li>");
                    li.text(data[i]["description"]);
                    li.attr("fid", data[i]["id"]);
                    li.attr("fname", data[i]["file_name"]);
                    li.attr("dpath", data[i]["downloading_path"]);
                    li.click(imit.FileManager.chooseFile);
                    ul.append(li);
                }
            });
    };

    var fm_form_submit = function (form) {
        var FD = new FormData(form.get(0));

        $.ajax({
            url: form.attr("action"),
            data: FD,//form.serialize(),
            type: 'POST',
            processData: false,
            contentType: false,
            cache: false,
            success: function (response) {
                console.log(response);
                imit.FileManager.updateFileManager();
            },
            error: function (error) {
                console.log(error);
            }
        });
    };

    this.addFile = function (event) {
        event.preventDefault();
        var $form = $(this);
        fm_form_submit($form);
    };

    this.removeFile = function (event) {
        event.preventDefault();
        var $form = $(this);
        fm_form_submit($form);
        $("#fm_edit_form").hide();
        $("#fm_remove_form").hide();
    };

    this.editFile = function (event) {
        event.preventDefault();
        var $form = $(this);
        fm_form_submit($form);
        $("#fm_edit_form").hide();
        $("#fm_remove_form").hide();
    };

    this.insertFileLink = function (event) {
        event.preventDefault();
        var fli = $("#fm_list").find("li[fid=" + window.fm_options.chosen_file + "]");
        var link = fli.attr("dpath");
        var a = "<a href='" + link + "'>" + fli.text() + "</a>";
        tinyMCE.execCommand('mceInsertContent', true, a);
    };

    this.copyFileLink = function (event) {
        event.preventDefault();
        var fli = $("#fm_list").find("li[fid=" + window.fm_options.chosen_file + "]");
        var link = fli.attr("dpath");
        $("#fm_copy_link_button").attr("data-clipboard-text", link);
    };

    $(function () {
        $("#fm_add_form").submit(imit.FileManager.addFile);
        $("#fm_edit_form").submit(imit.FileManager.editFile);
        $("#fm_remove_form").submit(imit.FileManager.removeFile);
        $("#fm_copy_link_button").click(imit.FileManager.copyFileLink);
        $("#fm_insert_link_button").click(imit.FileManager.insertFileLink);
    });

    return this;
}).call(imit.FileManager || {}, jQuery);

$(function initMagnificPopup() {
    /*$.extend(true, $.magnificPopup.defaults, {
        tClose: 'Закрыть (Esc)', // Alt text on close button
        tLoading: 'Загрузка...', // Text that is displayed during loading. Can contain %curr% and %total% keys
        gallery: {
            tPrev: 'Предыдущая (<-)', // Alt text on left arrow
            tNext: 'Следующая (->)', // Alt text on right arrow
            tCounter: '%curr% из %total%' // Markup for "1 of 7" counter
        },
        image: {
            tError: 'Не удалось загрузить <a href="%url%">изображение</a>.' // Error message when image could not be loaded
        }
    });*/
});


$(function initGallery() {
    /*$('.post-content').each(function () {
        $(this).magnificPopup({
            type: 'image',
            delegate: 'img',
            image: {
                titleSrc: 'alt'
            },
            gallery: {
                enabled: true
            },
            callbacks: {
                elementParse: function (item) {
                    var full = item.el.attr('full-cover-image');
                    if (full == null || full == undefined) {
                        item.src = item.el.attr('src');
                    } else {
                        item.src = full;
                    }
                }
            }
        });
    });*/
});


/**
 * menu
 */
imit.menu = (function ($) {
    /**
     * Hide/show menu in mobile version.
     */
    this.toggleMobileMenu = function (input) {
        console.log('from mobile menu');
        var x = document.getElementById("menu-mobile");
        if (x.className === "topnav") {
            x.className += " responsive";
        } else {
            x.className = "topnav";
        }
    }
    return this;
}).call(imit.menu || {}, jQuery);
