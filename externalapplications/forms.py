import logging
import taggit

from django import forms
from django.utils.translation import gettext as _
from .models import ExternalApplication

logger = logging.getLogger(__name__)


class ExternalApplicationCreateForm(forms.Form):
    title = forms.CharField(
        label=_("Title"),
        max_length=2000,
        widget=forms.TextInput(
            attrs={
                "size": "65",
                "class": "inputText",
                "required": "",
            }
        ),
    )
    abstract = forms.CharField(
        label=_("Abstract"),
        max_length=2000,
        widget=forms.TextInput(
            attrs={
                "size": "65",
                "class": "inputText",
                "required": "",
            }
        ),
    )
    url = forms.CharField(
        label=_("External Application URL"),
        max_length=2000,
        widget=forms.TextInput(
            attrs={
                "size": "65",
                "class": "inputText",
                "required": "",
                "type": "url",
            }
        ),
    )
    thumbnail = forms.FileField(
        label=_("Upload Thumbnail"),
        widget=forms.FileInput(
            attrs={
                "size": "65",
                "class": "inputText",
                "required": "false",
                "type": "file",
            }
        ),
    )


class ExternalApplicationForm(forms.ModelForm):
    title = forms.CharField(
        label=_("Title"),
        max_length=2000,
        widget=forms.TextInput(
            attrs={
                "size": "65",
                "class": "inputText",
                "required": "",
            }
        ),
    )
    abstract = forms.CharField(
        label=_("Abstract"),
        max_length=2000,
        widget=forms.TextInput(
            attrs={
                "size": "65",
                "class": "inputText",
                "required": "",
            }
        ),
    )
    url = forms.CharField(
        label=_("External Application URL"),
        max_length=2000,
        widget=forms.TextInput(
            attrs={
                "size": "65",
                "class": "inputText",
                "required": "",
                "type": "url",
            }
        ),
    )
    thumbnail = forms.FileField(
        label=_("Upload Thumbnail"),
        widget=forms.FileInput(
            attrs={
                "size": "65",
                "class": "inputText",
                "required": "",
                "type": "file",
            }
        ),
    )
    keywords = taggit.forms.TagField(required=False)

    class Meta:
        model = ExternalApplication
        fields = (
            "title",
            "abstract",
            "url",
            "thumbnail",
            "keywords",
        )
