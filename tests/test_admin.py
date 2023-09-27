from __future__ import annotations

import pytest

from reporting_endpoints.models import Report


pytestmark = pytest.mark.django_db


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        username="admin",
        password="hunter42",
        is_active=True,
        is_staff=True,
        is_superuser=True,
    )


def test_admin__listview(client, admin):
    client.force_login(admin)

    response = client.get("/admin/reporting_endpoints/")

    assert response.status_code == 200


def test_admin__changeview(client, admin):
    client.force_login(admin)

    report = Report.objects.create(
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

    response = client.get(f"/admin/reporting_endpoints/report/{report.id}/change/")

    assert response.status_code == 200
    assert str(report) in response.content.decode()
