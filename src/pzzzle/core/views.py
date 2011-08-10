# -*- coding: utf-8 -*-

import Image
from StringIO import StringIO
import os
import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Context, loader
from django.forms import *
from django.core.urlresolvers import reverse

from core import screenshot
from core import locks


def render_to_response(request, template_name, context_dict={}, cookies={}):
    context = RequestContext(request, context_dict)
    t = loader.get_template(template_name)
    response = HttpResponse(t.render(context))
    for k, v in cookies.items():
        response.set_cookie(k, v)
    return response


def index(request, message=None):
    cells = locks.get_cells_lock()
    for cell in cells:
        cell['url'] = settings.MEDIA_URL + 'data/%s_%s.jpg' % (cell['x'], cell['y'])
        cell['elapsed'] = cell['lock'] and u"%d мин" % ((settings.CELL_LOCK_PERIOD - cell['lock']) / 60) or ""
        cell['x'] = make_twodigit(cell['x'])
    
    context = {
        'cells': cells,
        'message': message,
        'request': request,
    }
    return render_to_response(request, 'index.html', context)


def upload(request):
    if request.FILES:
        x, y = get_point(request.POST)
        if not locks.get_cell_lock(x, y):
            thumb = resize(StringIO(request.FILES['pic'].read()))
            thumb.save(os.path.join(settings.THUMBNAIL_PATH, '%s_%s.jpg' % (x, y)))

            log = get_logger('upload')
            log.info('%s (%s, %s)', request.META['REMOTE_ADDR'], x, y)
        if request.POST.get('ajax'):
            return render_to_response(request, 'upload_complete.html', {'x': x, 'y': y, 'iframe': request.POST['iframe_name']})
        else:
            return HttpResponseRedirect('/')

    else:
        x, y = get_point(request.GET)

        return render_to_response(request, 'upload.html', {'x': x, 'y': y, 'request': request})


def resize(img):
    im = Image.open(img)
    im = make_square(im)
    im.thumbnail(settings.THUMBNAIL_SIZE, Image.ANTIALIAS)
    return im


def make_square(img):
    min_size = min(img.size)
    return img.crop((0, 0, min_size, min_size))


def lock(request):
    x, y = get_point(request.GET)
    ip = request.META['REMOTE_ADDR']
    try:
        res = locks.lock_cell(ip, x, y)
        if res[0]:
            return HttpResponse('success')
        else:
            return HttpResponse(res[1])
    except locks.LockError:
        return HttpResponse(u"Не шмогла :(")


def get_logger(name):
    filename = os.path.join(settings.LOG_PATH, name.replace('.', '/') + '.log')

    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
                  filename, maxBytes=10000000, backupCount=10)
    LOG_FORMAT = u'%(levelname)s %(asctime)s: %(message)s'
    LOG_TIME_FORMAT = u'%Y-%m-%d %H:%M:%S'
    handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_TIME_FORMAT))
    log.addHandler(handler)

    return log


def get_point(query_dict):
    class PointForm(Form):
        x = CharField(required=False, max_length=100)
        y = CharField(required=False, max_length=100)

        def clean_x(self):
            try:
                return min(max(int(self.cleaned_data.get('x', 1)), 1), settings.TABLE[0])
            except (ValueError, TypeError, OverflowError):
                return 1

        def clean_y(self):
            try:
                return min(max(int(self.cleaned_data.get('y', 1)), 1), settings.TABLE[1])
            except (ValueError, TypeError, OverflowError):
                return 1

    point_form = PointForm(query_dict)
    point_form.is_valid()
    return point_form.cleaned_data['x'], point_form.cleaned_data['y']


def make_twodigit(number):
    if number < 10:
        return '0%s' % number
    else:
        return str(number)


def screenshot_make(request):
    if not request.POST:
        raise Http404
    
    try:
        screenshot.make_screenshot(request.META['REMOTE_ADDR'])
        return HttpResponseRedirect(reverse('screenshot_view', args=[1]))
    
    except screenshot.NotAllowed:
        return index(request, message=u"Генерация скриншотов разрешена раз в час.")
    except screenshot.LockError:
        return index(request, message=u"Ошибка блокировки. Попробуйте еще раз.")

    
def screenshot_view(request, page):
    number = screenshot.get_current_number() + int(page) - 1
    return render_to_response(request, 'screenshot.html', {'number': number})