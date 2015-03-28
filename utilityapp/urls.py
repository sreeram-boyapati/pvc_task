from django.conf.urls import patterns, include, url
from utilityapp.views import test_model_view, train_model_view

urlpatterns = patterns(
    '',
    url(r'^utility/test_model/$', test_model_view),
    url(r'^utility/train_model/$', train_model_view),
)
