from django.conf.urls import patterns, include, url
# from core.views import test_model_view, train_model_view, fetch_images
from core.views import fetch_images

urlpatterns = patterns(
    '',
    # url(r'^test_model/$', test_model_view),
    # url(r'^train_model/$', train_model_view),
    url(r'fetch_images/(?P<category>[\w\-\+]+)/$', fetch_images),
)
