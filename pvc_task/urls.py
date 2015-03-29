from django.conf.urls import patterns, include, url
import core
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from homepage.views import get_homepage
urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', get_homepage, name='home'),
    # url(r'^pvc_task/', include('pvc_task.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^core/', include('core.urls')),
    url(r'^accounts/', include('allauth.urls')),

)
