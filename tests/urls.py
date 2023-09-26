from __future__ import annotations

from django.http import HttpResponse
from django.urls import path

from reporting_endpoints.views import reporting_endpoint


def index(request):
    return HttpResponse("OK")


urlpatterns = [
    path("", index),
    path(
        "_/csp-reports/", reporting_endpoint, kwargs={"endpoint_name": "csp-violations"}
    ),
]
