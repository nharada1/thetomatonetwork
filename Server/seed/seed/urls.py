from django.conf.urls import patterns, include, url
from django.contrib import admin
from seed import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
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
    url(r'^analytics', 'plants.views.analytics'),
    url(r'^update','plants.views.update_performance'),
    url(r'^runalgo','plants.views.update_nutrients'),
    url(r'^sync','plants.views.sync'),
    url(r'^stream','plants.views.stream'),
    url(r'', 'plants.views.index'),

)

urlpatterns += staticfiles_urlpatterns()
