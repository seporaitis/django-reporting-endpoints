from __future__ import annotations

from django.contrib import admin

from reporting_endpoints.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    readonly_fields = [
        "age",
        "blocked_uri",
        "column_number",
        "created_at",
        "disposition",
        "document_uri",
        "effective_directive",
        "endpoint_name",
        "line_number",
        "original_policy",
        "referrer",
        "type",
        "sample",
        "source_file",
        "status_code",
        "url",
        "user_agent",
        "violated_directive",
    ]
    list_display = [
        "endpoint_name",
        "created_at",
        "disposition",
        "effective_directive",
        "blocked_uri",
    ]
    list_filter = [
        "endpoint_name",
        "disposition",
        "effective_directive",
        "violated_directive",
        "status_code",
        "type",
    ]
    fieldsets = [
        (
            "Delivery Metadata",
            {
                "fields": [
                    "created_at",
                    ("endpoint_name", "type"),
                    "age",
                    "url",
                    "user_agent",
                ]
            },
        ),
        (
            "Report",
            {
                "fields": [
                    "disposition",
                    "blocked_uri",
                    "document_uri",
                    "effective_directive",
                    "original_policy",
                    "referrer",
                    "status_code",
                    "violated_directive",
                ]
            },
        ),
        (
            "Sample",
            {"fields": [("source_file", "line_number", "column_number"), "sample"]},
        ),
    ]
