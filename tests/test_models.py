import pytest

from reporting_endpoints.models import Report

pytestmark = pytest.mark.django_db


def test_str():
    report = Report.objects.create(
        id=1,
        endpoint_name="test-suite",
        age=0,
        type="csp-violation",
        url="https://example.com/",
        user_agent="test-client",
        blocked_uri="https://example.org/",
        disposition="report",
        document_uri="https://example.com/",
        effective_directive="script-src-elem",
        original_policy="script-src 'self'",
        referrer="",
        sample="",
        status_code=200,
    )

    assert str(report) == "Report(disposition=report, id=1)"
