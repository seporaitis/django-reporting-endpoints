from __future__ import annotations

import json

import pytest

from reporting_endpoints.models import Report


pytestmark = pytest.mark.django_db


def test_unparseable(client):
    response = client.post(
        "/_/csp-reports/",
        data="YOLO",
        content_type="application/csp-report",
    )

    assert response.status_code == 400
    assert response.content.decode() == "could not parse"


def test_incorrect_content_type(client):
    response = client.post(
        "/_/csp-reports/",
        data="null",
        content_type="application/text",
    )

    assert response.status_code == 400
    assert response.content.decode() == "incorrect content type"


@pytest.mark.parametrize("disposition", ["enforce", "report", "unknown"])
def test_csp_report(client, disposition):
    data = {
        "document-uri": "https://example.com",
        "referrer": "",
        "violated-directive": "script-src-elem",
        "effective-directive": "script-src-elem",
        "original-policy": "script-src 'self'",
        "disposition": disposition,
        "blocked-uri": "inline",
        "status-code": 200,
    }
    response = client.post(
        "/_/csp-reports/",
        data=json.dumps({"csp-report": data}),
        content_type="application/csp-report",
    )

    assert response.status_code == 201

    report = Report.objects.get()

    assert report.age is None
    assert report.type is None
    assert report.url is None
    assert report.user_agent is None
    assert report.document_uri == data["document-uri"]
    assert report.referrer == data["referrer"]
    assert report.violated_directive == data["violated-directive"]
    assert report.effective_directive == data["effective-directive"]
    assert report.original_policy == data["original-policy"]
    assert report.disposition == disposition
    assert report.blocked_uri == data["blocked-uri"]
    assert report.status_code == data["status-code"]
    assert report.sample == ""


def test_csp_report__value_too_long(client):
    data = {
        "document-uri": "https://example.com" + "A" * 1024,
        "referrer": "",
        "violated-directive": "script-src-elem",
        "effective-directive": "script-src-elem",
        "original-policy": "script-src 'self'",
        "disposition": "enforce",
        "blocked-uri": "inline",
        "status-code": 200,
    }
    response = client.post(
        "/_/csp-reports/",
        data=json.dumps({"csp-report": data}),
        content_type="application/csp-report",
    )

    assert response.status_code == 201

    report = Report.objects.get()

    assert report.age is None
    assert report.type is None
    assert report.url is None
    assert report.user_agent is None
    assert report.document_uri == data["document-uri"][:1021] + "..."
    assert report.referrer == data["referrer"]
    assert report.violated_directive == data["violated-directive"]
    assert report.effective_directive == data["effective-directive"]
    assert report.original_policy == data["original-policy"]
    assert report.disposition == data["disposition"]
    assert report.blocked_uri == data["blocked-uri"]
    assert report.status_code == data["status-code"]
    assert report.sample == ""


def test_single_report(client):
    data = {
        "age": 1000,
        "type": "csp-violation",
        "url": "https://example.com/",
        "user_agent": "test-client",
        "body": {
            "documentURL": "https://example.com",
            "referrer": "",
            "violatedDirective": "script-src-elem",
            "effectiveDirective": "script-src-elem",
            "originalPolicy": "script-src 'self'",
            "disposition": "enforce",
            "blockedURL": "inline",
            "statusCode": 200,
            "sample": "piece of code",
        },
    }
    response = client.post(
        "/_/csp-reports/",
        data=json.dumps(data),
        content_type="application/reports+json",
    )

    assert response.status_code == 201

    report = Report.objects.get()

    assert report.age == data["age"]
    assert report.type == data["type"]
    assert report.url == data["url"]
    assert report.user_agent == data["user_agent"]
    assert report.document_uri == data["body"]["documentURL"]
    assert report.referrer == data["body"]["referrer"]
    assert report.violated_directive == ""
    assert report.effective_directive == data["body"]["effectiveDirective"]
    assert report.original_policy == data["body"]["originalPolicy"]
    assert report.disposition == data["body"]["disposition"]
    assert report.blocked_uri == data["body"]["blockedURL"]
    assert report.status_code == data["body"]["statusCode"]
    assert report.sample == data["body"]["sample"]


def test_single_report__value_too_long(client):
    data = {
        "age": 1000,
        "type": "csp-violation",
        "url": "https://example.com/" + "A" * 1024,
        "user_agent": "test-client",
        "body": {
            "documentURL": "https://example.com" + "A" * 1024,
            "referrer": "",
            "violatedDirective": "script-src-elem",
            "effectiveDirective": "script-src-elem",
            "originalPolicy": "script-src 'self'",
            "disposition": "enforce",
            "blockedURL": "inline",
            "statusCode": 200,
            "sample": "piece of code",
        },
    }
    response = client.post(
        "/_/csp-reports/",
        data=json.dumps(data),
        content_type="application/reports+json",
    )

    assert response.status_code == 201

    report = Report.objects.get()

    assert report.age == data["age"]
    assert report.type == data["type"]
    assert report.url == data["url"][:1021] + "..."
    assert report.user_agent == data["user_agent"]
    assert report.document_uri == data["body"]["documentURL"][:1021] + "..."
    assert report.referrer == data["body"]["referrer"]
    assert report.violated_directive == ""
    assert report.effective_directive == data["body"]["effectiveDirective"]
    assert report.original_policy == data["body"]["originalPolicy"]
    assert report.disposition == data["body"]["disposition"]
    assert report.blocked_uri == data["body"]["blockedURL"]
    assert report.status_code == data["body"]["statusCode"]
    assert report.sample == data["body"]["sample"]


def test_multiple_reports(client):
    data = {
        "age": 1000,
        "type": "csp-violation",
        "url": "https://example.com/",
        "user_agent": "test-client",
        "body": {
            "documentURL": "https://example.com",
            "referrer": "",
            "violatedDirective": "script-src-elem",
            "effectiveDirective": "script-src-elem",
            "originalPolicy": "script-src 'self'",
            "disposition": "enforce",
            "blockedURL": "inline",
            "statusCode": 200,
            "sample": "piece of code",
        },
    }
    response = client.post(
        "/_/csp-reports/",
        data=json.dumps([data, data, data]),
        content_type="application/reports+json",
    )

    assert response.status_code == 201
    assert Report.objects.count() == 3

    for report in Report.objects.all():
        assert report.age == data["age"]
        assert report.type == data["type"]
        assert report.url == data["url"]
        assert report.user_agent == data["user_agent"]
        assert report.document_uri == data["body"]["documentURL"]
        assert report.referrer == data["body"]["referrer"]
        assert report.violated_directive == ""
        assert report.effective_directive == data["body"]["effectiveDirective"]
        assert report.original_policy == data["body"]["originalPolicy"]
        assert report.disposition == data["body"]["disposition"]
        assert report.blocked_uri == data["body"]["blockedURL"]
        assert report.status_code == data["body"]["statusCode"]
        assert report.sample == data["body"]["sample"]


def test_multiple_reports__value_too_long(client):
    data = {
        "age": 1000,
        "type": "csp-violation",
        "url": "https://example.com/" + "A" * 1024,
        "user_agent": "test-client",
        "body": {
            "documentURL": "https://example.com" + "A" * 1024,
            "referrer": "",
            "violatedDirective": "script-src-elem",
            "effectiveDirective": "script-src-elem",
            "originalPolicy": "script-src 'self'",
            "disposition": "enforce",
            "blockedURL": "inline",
            "statusCode": 200,
            "sample": "piece of code",
        },
    }
    response = client.post(
        "/_/csp-reports/",
        data=json.dumps([data, data, data]),
        content_type="application/reports+json",
    )

    assert response.status_code == 201
    assert Report.objects.count() == 3

    for report in Report.objects.all():
        assert report.age == data["age"]
        assert report.type == data["type"]
        assert report.url == data["url"][:1021] + "..."
        assert report.user_agent == data["user_agent"]
        assert report.document_uri == data["body"]["documentURL"][:1021] + "..."
        assert report.referrer == data["body"]["referrer"]
        assert report.violated_directive == ""
        assert report.effective_directive == data["body"]["effectiveDirective"]
        assert report.original_policy == data["body"]["originalPolicy"]
        assert report.disposition == data["body"]["disposition"]
        assert report.blocked_uri == data["body"]["blockedURL"]
        assert report.status_code == data["body"]["statusCode"]
        assert report.sample == data["body"]["sample"]
