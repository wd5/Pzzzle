# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from core.views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^upload', upload),
    url(r'^lock', lock),
    url(r'^screentshots/(\d+)', screenshot_view, name='screenshot_view'),
    url(r'^screentshots/make', screenshot_make, name='screenshot_make'),
)

