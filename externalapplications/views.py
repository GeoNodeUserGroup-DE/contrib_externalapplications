import uuid
import logging
from io import BytesIO
from PIL import Image

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from geonode.resource.manager import resource_manager
from .forms import ExternalApplicationCreateForm
from .models import ExternalApplication

logger = logging.getLogger(__name__)


def external_applications_list(request):
    template = "externalapplications/externalapplications_list.html"
    return render(request, template)


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
            resource_manager.set_permissions(None, instance=obj, permissions=None, created=True)

            if form.files and form.files["thumbnail"]:
                thumbnail = form.files["thumbnail"]
                with BytesIO() as output:
                    img = Image.open(thumbnail)
                    img.save(output, format="PNG")
                    content = output.getvalue()
                obj.save_thumbnail(thumbnail.name, content)
        return HttpResponseRedirect(reverse("external_applications_list"))
    else:
        form = ExternalApplicationCreateForm()
        result = render(request, template, {"form": form})
        return result
