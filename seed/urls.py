from django.conf.urls import patterns, include, url
from django.contrib import admin
from seed import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'seed.views.home', name='home'),
    #url(r'^seed/', include('seed.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Allow admin to display
urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
 )