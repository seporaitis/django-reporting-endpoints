from __future__ import annotations

from django.db import models


class Report(models.Model):
    class Disposition(models.TextChoices):
        ENFORCE = "enforce"
        REPORT = "report"
        UNKNOWN = "unknown"

    created_at = models.DateTimeField(auto_now_add=True)
    endpoint_name = models.CharField(max_length=1024, null=True, blank=True)

    age = models.PositiveIntegerField(null=True, blank=True)
    type = models.CharField(max_length=256, null=True, blank=True)
    url = models.CharField(max_length=1024, null=True, blank=True)
    user_agent = models.CharField(max_length=1024, null=True, blank=True)

    blocked_uri = models.CharField(max_length=1024)
    disposition = models.CharField(max_length=128, choices=Disposition.choices)
    document_uri = models.CharField(max_length=1024)
    effective_directive = models.CharField(max_length=1024)
    original_policy = models.TextField()
    referrer = models.CharField(max_length=1024)
    status_code = models.PositiveIntegerField()
    violated_directive = models.CharField(max_length=1024)
    sample = models.CharField(max_length=1024)
    source_file = models.CharField(max_length=1024, null=True, blank=True)
    line_number = models.PositiveIntegerField(null=True, blank=True)
    column_number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Report(disposition={self.disposition}, id={self.id})"
