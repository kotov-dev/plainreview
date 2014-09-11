from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from plainreview.apps.core.views import upload_review, home

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^upload-review/', upload_review, name='upload_review'),
    url(r'^admin/', include(admin.site.urls)),
)
