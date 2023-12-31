from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/?$', views.create_external_application, name='external_application_create'),
    url(r'^(?P<appid>[^/]+)/metadata_detail$', views.external_application_metadata_detail,
        name='external_application_metadata_detail'),
]
