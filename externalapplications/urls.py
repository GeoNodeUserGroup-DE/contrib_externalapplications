from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^create/?$", views.create_external_application, name="external_application_create"),
]
