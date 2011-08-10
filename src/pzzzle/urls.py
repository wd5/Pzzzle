
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^', include('core.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
     )

