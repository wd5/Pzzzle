$(document).ready(function () {
    $('#uploader').hide();
});


$(window).load(function () {
    function left(str, n) {
        if (n <= 0) return "";
        else if (n > String(str).length) return str;
        else return String(str).substring(0, n);
    }

    window.upload_complete = function(x,y, iframe_name) {
      var img = new Image();
      $(img).load(function () {
          $(this).hide();
          $('#preview').append(this);
          $(this).fadeIn();
      }).error(function () {
          alert('ÙÈ!');
      }).attr('src', '/media/data/' + x + '_' + y + '.jpg');
      
      console.log(iframe_name);
      $('#' + iframe_name).remove();
      
      var new_x = (x < 10) ? ('0' + x) : x;
      
      $('#cell_image_' + new_x + '_' + y).attr('src', '/media/data/' + x + '_' + y + '.jpg?random=' + Math.random());
      console.log('completeCallback done');
      $('.close').trigger('upload:complete');
      return true;
    }

    function right(str, n) {
        if (n <= 0) return "";
        else if (n > String(str).length) return str;
        else {
            var iLen = String(str).length;
            return String(str).substring(iLen, iLen - n);
        }
    }

    var wrapper = $('#mousepad');
    var content = $('#cursor-touch');

    wrapper.bind('mouseenter mousemove', $.throttle(500, buildThumbs));

    function buildThumbs(e) {
        var wrapper_width = wrapper.outerWidth();
        var content_width = content.outerWidth();
        var inactiveMargin = 50;
        var left = (e.pageX - $('#mousepad').offset().left) * (content_width - wrapper_width) / wrapper_width - inactiveMargin;
        content.stop().animate({
            'margin-left': '-' + left + 'px'
        }, 500);
        $('#imagery-outer').stop().animate({
            scrollLeft: left
        }, 500);
    }
    $('#imagery-inner>div').mouseover(function () {
        $('#imagery-inner>div').css('z-index', 1);
        $(this).css('z-index', 10);
        $(this).find('.hovering').stop().animate({
            'opacity': 1
        }, 400);
    });
    $('#imagery-inner>div').mouseleave(function () {
        $(this).css('z-index', 1);
        $(this).find('.hovering').stop().animate({
            'opacity': 0
        }, 200);
    });
    $('.upload').click(function () {
        $('.splasher').css('display', 'block').stop().animate({
            'opacity': 0.75
        }, 400);
        $('#modal').css('display', 'block').stop().animate({
            'opacity': 1
        }, 900)
        var target = $(this).find('a').attr('class').split(' ');
        console.log(target);
        for (x = 0; x <= target.length; x++) {
            if (left(target[x], 1) == "x") {
                $('form').find("#absciss").attr('value', right(target[x], 2));
            }
            if (left(target[x], 1) == "y") {
                $('form').find("#ordinat").attr('value', right(target[x], 1));
            }
        }
    });
    $('.close').bind('upload:complete click', function () {
        $('#modal').animate({
            'opacity': 0
        }, {
            duration: 400,
            complete: function () {
                $(this).css("display", "none")
            }
        });
        $('.splasher').animate({
            'opacity': 0
        }, {
            duration: 400,
            complete: function () {
                $(this).css("display", "none")
            }
        });
    })

    var fileInput = document.getElementById('File1');
    var fileName = document.createElement('div');
    var submit = document.getElementById('push');
    var activeButton = document.createElement('div');
    var bb = document.createElement('div');
    var sendme = document.createElement('div');
    WindowOnLoad()

    function WindowOnLoad() {
        var wrap = document.getElementById('push-up');
        fileName.setAttribute('id', 'FileName');
        activeButton.setAttribute('id', 'activeBrowseButton');
        fileInput.value = '';
        fileInput.onchange = HandleChanges;
        fileInput.onmouseover = MakeActive;
        fileInput.onmouseout = UnMakeActive;
        submit.className = 'customFile';
        fileInput.className = 'customFile';
        bb.className = 'fakeButton';
        activeButton.className = 'fakeButton';
        sendme.className = 'fakeSubmit';
        wrap.appendChild(bb);
        wrap.appendChild(activeButton);
        wrap.appendChild(fileName);
        wrap.appendChild(sendme);
    };

    function HandleChanges() {
        file = fileInput.value;
        reWin = /.*\\(.*)/;
        var fileTitle = file.replace(reWin, "$1");
        reUnix = /.*\/(.*)/;
        fileTitle = fileTitle.replace(reUnix, "$1");
        fileName.innerHTML = fileTitle;

        var RegExExt = /.*\.(.*)/;
        var ext = fileTitle.replace(RegExExt, "$1");

        var pos;
        if (ext) {
            switch (ext.toLowerCase()) {
            case 'bmp':
                pos = '16';
                break;
            case 'jpg':
                pos = '32';
                break;
            case 'jpeg':
                pos = '32';
                break;
            case 'png':
                pos = '48';
                break;
            case 'gif':
                pos = '64';
                break;
            case 'psd':
                pos = '80';
                break;
            default:
                pos = '176';
                break;
            };

        };

    };

    function MakeActive() {
        activeButton.style.display = 'block';
    };

    function UnMakeActive() {
        activeButton.style.display = 'none';
    };

    function disableActions() {
        var links = document.getElementsByTagName("a");
        for (i = 0; i < links.length; i++) {
            var link = links[i];
            link.onclick = function () {
                return false;
            }
        }
    }
    disableActions();

    $('#push-up').submit(function () {
      //display uploading progress bar
      var iframe_name = 'iframe_' + Math.random().toString().replace('.', '');
      var iframe = $('<iframe name="' + iframe_name + '" id="' + iframe_name + '" class="hidden-iframe"></iframe>');
      $('body').append(iframe);
      $('#push-up').attr('target', iframe_name).find('#iframe_name').val(iframe_name);
    })

    function startCallback() {
        // make something useful before submit (onStart)
        console.log('startCallback done');
        return true;
    }

    function completeCallback() {

        // make something useful after (onComplete)
        var xcoor = $("#absciss").attr('value');
        var ycoor = $("#ordinat").attr('value');
        if (xcoor[0] == "0") {
            xcoor = xcoor.substr(1, xcoor.length);
        }
        var img = new Image();
        $(img).load(function () {
            $(this).hide();
            $('#preview').append(this);
            $(this).fadeIn();
        }).error(function () {
            alert('ÙÈ!');
        }).attr('src', '/media/data/' + xcoor + '_' + ycoor + '.jpg');
        console.log('completeCallback done');
        return true;
    }

    function lock(x, y) {
        console.log('CLICK');
        $.get('/lock', {
            x: x,
            y: y
        }, function (result) {
            if (result == 'success') {
                $('#control_' + x + '_' + y).html('10 min <img src="/media/i/protected.png">');
            } else {
                alert(result);
            }
        });
        return false;
    }
});