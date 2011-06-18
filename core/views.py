# -*- coding: utf-8 -*-

import Image
from StringIO import StringIO
import os
import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.template import RequestContext, Context, loader

def render_to_response(request, template_name, context_dict={}, cookies={}):
    context = RequestContext(request, context_dict)
    t = loader.get_template(template_name)
    response = HttpResponse(t.render(context))
    for k, v in cookies.items():
        response.set_cookie(k, v)
    return response


def index(request):
    context = {
        'cells': [ [{'x': x+1, 'y': y+1, 'url': settings.MEDIA_URL + 'data/%s_%s.jpg' % (x+1, y+1)} for x in xrange(settings.TABLE[0])] for y in xrange(settings.TABLE[1])]
    }
    return render_to_response(request, 'index.html', context)


def upload(request):
    try:
        x = int(request.GET['x'])
    except (KeyError, ValueError):
        x = 1
    if x > settings.TABLE[0] or x < 1:
        x = 1
    try:
        y = int(request.GET['y'])
    except (KeyError, ValueError):
        y = 1
    if y > settings.TABLE[1] or y < 1:
        y = 1

    if request.FILES:
        thumb = resize(StringIO(request.FILES['pic'].read()))
        thumb.save(os.path.join(settings.THUMBNAIL_PATH, '%s_%s.jpg' % (x, y)))

        log = get_logger('upload')
        log.info('%s (%s, %s)', request.META['REMOTE_ADDR'], x, y)
        return HttpResponseRedirect('/')

    else:
        return render_to_response(request, 'upload.html', {'x': x, 'y': y})


def resize(img):
    im = Image.open(img)
    im = make_square(im)
    im.thumbnail(settings.THUMBNAIL_SIZE, Image.ANTIALIAS)
    return im


def make_square(img):
    min_size = min(img.size)
    return img.crop((0, 0, min_size, min_size))

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
