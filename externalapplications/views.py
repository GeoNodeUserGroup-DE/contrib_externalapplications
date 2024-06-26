import uuid
import logging
from io import BytesIO
from PIL import Image

from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from django.forms.utils import ErrorList
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from geonode.utils import resolve_object
from geonode.base import register_event
from geonode.groups.models import GroupProfile
from geonode.monitoring.models import EventType
from geonode.resource.manager import resource_manager
from .forms import ExternalApplicationCreateForm
from .models import ExternalApplication

_PERMISSION_MSG_GENERIC = _(
    "You do not have permissions for this external application."
)
_PERMISSION_MSG_METADATA = _(
    "You are not permitted to modify this external application's metadata"
)

logger = logging.getLogger(__name__)


@login_required
def create_external_application(request):
    template = "externalapplications/external_application_create.html"

    if request.method == "POST":

        form = ExternalApplicationCreateForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            obj = ExternalApplication.objects.create(
                owner=request.user,
                url=data.get("url"),
                title=data.get("title"),
                abstract=data.get("abstract"),
                uuid=str(uuid.uuid4()),
                resource_type="externalapplication",
            )

            obj.set_missing_info()
            resource_manager.set_permissions(
                None, instance=obj, permissions=None, created=True
            )

            if form.files and form.files["thumbnail"]:
                thumbnail = form.files["thumbnail"]
                with BytesIO() as output:
                    img = Image.open(thumbnail)
                    img.save(output, format="PNG")
                    content = output.getvalue()
                obj.save_thumbnail(thumbnail.name, content)
        return HttpResponseRedirect(
            reverse("external_application_metadata_detail", args=(obj.pk,))
        )
    else:
        form = ExternalApplicationCreateForm()
        result = render(request, template, {"form": form})
        return result


def _resolve_external_application(
    request,
    appid,
    permission="base.change_resourcebase",
    msg=_PERMISSION_MSG_GENERIC,
    **kwargs
):
    """
    Resolve the external application by the provided primary key and check
    the optional permission.
    """
    return resolve_object(
        request,
        ExternalApplication,
        {"pk": appid},
        permission=permission,
        permission_msg=msg,
        **kwargs
    )


def external_application_metadata_detail(
    request,
    appid,
    template="externalapplications/external_application_metadata_detail.html",
):
    try:
        external_application = _resolve_external_application(
            request, appid, "view_resourcebase", _PERMISSION_MSG_METADATA
        )
    except PermissionDenied:
        return HttpResponse(_("Not allowed"), status=403)
    except Exception:
        raise Http404(_("Not found"))
    if not external_application:
        raise Http404(_("Not found"))

    group = None
    if external_application.group:
        try:
            group = GroupProfile.objects.get(slug=external_application.group.name)
        except ObjectDoesNotExist:
            group = None
    site_url = (
        settings.SITEURL.rstrip("/")
        if settings.SITEURL.startswith("http")
        else settings.SITEURL
    )
    register_event(request, EventType.EVENT_VIEW_METADATA, external_application)
    return render(
        request,
        template,
        context={
            "resource": external_application,
            "group": group,
            "SITEURL": site_url
        },
    )
