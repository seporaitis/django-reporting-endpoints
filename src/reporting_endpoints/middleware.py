from __future__ import annotations

import json
from typing import Callable

from django.conf import settings
from django.http import HttpRequest
from django.http.response import HttpResponseBase


class ReportingEndpointsMiddleware:
    sync_capable = True
    async_capable = False

    def __init__(
        self,
        get_response: (Callable[[HttpRequest], HttpResponseBase]),
    ) -> None:
        self.get_response = get_response

    def _prepare_reporting_endpoints(self) -> str | None:
        endpoints = getattr(settings, "REPORTING_ENDPOINTS", None)
        if endpoints is None:
            return endpoints
        if isinstance(endpoints, str):
            return endpoints

        endpoint = '{name}="{url}"'.format
        return ",".join(
            [endpoint(name=name, url=url) for name, url in endpoints.items()]
        )

    def _prepare_report_to_endpoints(self) -> str | None:
        endpoints = getattr(settings, "REPORT_TO_ENDPOINTS", None)
        if endpoints is None:
            return endpoints
        if isinstance(endpoints, str):
            return endpoints

        if isinstance(endpoints, dict):
            endpoints = [endpoints]

        return ",".join([json.dumps(endpoint) for endpoint in endpoints])

    def __call__(self, request: HttpRequest) -> HttpResponseBase:
        response = self.get_response(request)

        reporting_endpoints = self._prepare_reporting_endpoints()
        if reporting_endpoints:
            response.headers["Reporting-Endpoints"] = reporting_endpoints
        report_to_endpoints = self._prepare_report_to_endpoints()
        if report_to_endpoints:
            response.headers["Report-To"] = report_to_endpoints

        return response
