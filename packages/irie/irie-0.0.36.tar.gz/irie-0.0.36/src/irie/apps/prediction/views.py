#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
#
#   This module implements the "Configure Predictors" page
#
#   Author: Claudio Perez
#
#----------------------------------------------------------------------------#
import os
import json

from django.shortcuts import HttpResponse
from django.template import loader, TemplateDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render

from irie.apps.site.view_utils import raise404
from irie.apps.inventory.models import Asset
from irie.apps.prediction.predictor import PREDICTOR_TYPES
from irie.apps.prediction.models import PredictorModel
from .forms import PredictorForm

@login_required(login_url="/login/")
def new_prediction(request):
    context = {}

    page_template = "form-submission.html"
    context["segment"] = page_template
    html_template = loader.get_template("prediction/" + page_template)
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def asset_predictors(request, calid):

    context = {"segment": "inventory"}

    context["runners"] = list(reversed([
        {
            "schema": json.dumps(cls.schema),
            "name":   cls.__name__,
            "title":  cls.schema.get("title", "NO TITLE"),
            "protocol":   key
        }
        for key,cls in PREDICTOR_TYPES.items() if key
    ]))


    try:
        context["asset"] = Asset.objects.get(calid=calid)

    except Asset.DoesNotExist:
        return HttpResponse(
                loader.get_template("site/page-404-sidebar.html").render(context, request)
               )

    html_template = loader.get_template("prediction/asset-predictors.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def predictor_profile(request, calid, preid):

    context = {}
    html_template = loader.get_template("prediction/predictor-profile.html")
    context["segment"] = "inventory"

    try:
        asset = Asset.objects.get(calid=calid)
    except Asset.DoesNotExist:
        return raise404(request, context)

    try:
        predictor = PredictorModel.objects.get(pk=int(preid))
    except ObjectDoesNotExist:
        return raise404(request, context)

    context["asset"] = asset
    context["predictor"] = PREDICTOR_TYPES[predictor.protocol](predictor)

    try:
        return HttpResponse(html_template.render(context, request))

    except TemplateDoesNotExist:
        context["rendering"] = None
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        if "DEBUG" in os.environ and os.environ["DEBUG"]:
            raise e
        html_template = loader.get_template("site/page-500.html")
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def predictor_upload(request, calid):

    html_template = loader.get_template("prediction/predictor-upload.html")

    if request.method == "POST":
        form = PredictorForm(request.POST, request.FILES)
        asset = Asset.objects.get(calid=calid)

        # Save the predictor
        predictor = PREDICTOR_TYPES[request.POST.get("runner")].create(asset, request)
        predictor.save()

        return HttpResponse(json.dumps({"data": {"id": predictor.id}}))

    else:
        form = PredictorForm()


    try:
        return render(request, "prediction/predictor-upload.html", {"form": form})

    except Exception as e:
        if "DEBUG" in os.environ and os.environ["DEBUG"]:
            raise e
        html_template = loader.get_template("site/page-500.html")
        return HttpResponse(html_template.render({}, request))


