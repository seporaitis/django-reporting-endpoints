from __future__ import annotations

import json

from django.http import HttpRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from reporting_endpoints.models import Report


def trim(value, length=1024):
    if len(value) > 1024:
        return value[: 1024 - 3] + "..."
    return value


@require_POST
@csrf_exempt
def reporting_endpoint(
    request: HttpRequest, endpoint_name: str | None = None
) -> HttpResponse:
    try:
        data = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return HttpResponse("could not parse", status=400)

    if request.headers["content-type"] not in (
        "application/csp-report",
        "application/reports+json",
    ):
        return HttpResponse("incorrect content type", status=400)

    if "csp-report" in data:
        report = data["csp-report"]
        disposition = Report.Disposition.UNKNOWN
        if report.get("disposition") == "enforce":
            disposition = Report.Disposition.ENFORCE
        elif report.get("disposition") == "report":
            disposition = Report.Disposition.REPORT
        Report.objects.create(
            endpoint_name=endpoint_name,
            document_uri=trim(report["document-uri"]),
            referrer=trim(report["referrer"]),
            violated_directive=report["violated-directive"],
            effective_directive=report["effective-directive"],
            original_policy=report["original-policy"],
            disposition=disposition,
            blocked_uri=report["blocked-uri"],
            status_code=report["status-code"],
            sample=trim(report.get("script-sample") or report.get("sample") or ""),
            source_file=report.get("source-file"),
            line_number=report.get("line-number"),
            column_number=report.get("column-number"),
        )
        return HttpResponse("", status=201)

    if not isinstance(data, list):
        data = [data]

    to_save = []
    for report in data:
        to_save.append(
            Report(
                endpoint_name=endpoint_name,
                age=report.get("age"),
                type=report.get("type"),
                url=trim(report.get("url")),
                user_agent=trim(report.get("user_agent")),
                blocked_uri=report["body"]["blockedURL"],
                disposition=report["body"]["disposition"],
                document_uri=trim(report["body"]["documentURL"]),
                effective_directive=report["body"]["effectiveDirective"],
                original_policy=report["body"]["originalPolicy"],
                referrer=trim(report["body"]["referrer"]),
                sample=trim(report["body"]["sample"]),
                status_code=report["body"]["statusCode"],
            )
        )

    Report.objects.bulk_create(to_save)

    return HttpResponse("", status=201)
