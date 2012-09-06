from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^sitespy/', include('sitespy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
        (r'^admin/', include(admin.site.urls)),
        (r'^$', "core.views.index"),
        (r'^search$', "core.views.search"),
        url(r'^view/(?P<d>.+)/$', 'core.views.view',name="view_domain"),
    

)

urlpatterns += staticfiles_urlpatterns()
