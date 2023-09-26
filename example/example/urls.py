from __future__ import annotations

from django.contrib import admin
from django.urls import path

from example import views
from reporting_endpoints.views import reporting_endpoint

urlpatterns = [
    path("", views.index),
    path("favicon.ico", views.favicon),
    path(
        "_/csp-reports/", reporting_endpoint, kwargs={"endpoint_name": "csp-violations"}
    ),
    path("admin/", admin.site.urls),
]
