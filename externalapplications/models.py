from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from geonode.geoapps.models import GeoApp


class ExternalApplication(GeoApp):

    url = models.URLField(
        max_length=2000,
        null=False,
        blank=False,
        help_text=_("Link to the external application"),
    )

    @property
    def embed_url(self):
        return None

    def get_absolute_url(self):
        return self.url


admin.site.register(ExternalApplication)
