from __future__ import annotations

from django.apps import AppConfig


class ReportingEndpointsConfig(AppConfig):
    name = "reporting_endpoints"
    verbose_name = "Policy Violation Reports"
    default_auto_field = "django.db.models.AutoField"
