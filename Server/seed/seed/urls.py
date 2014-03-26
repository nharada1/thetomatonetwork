from django.conf.urls import patterns, include, url
from django.contrib import admin
from seed import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'seed.views.home', name='home'),
    #url(r'^seed/', include('seed.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
    url(r'^update','plants.views.update_performance'),
    url(r'^runalgo','plants.views.update_nutrients'),
    url(r'^$','plants.views.index'),
    url(r'^query_arduino','plants.view.query_arduino')
)