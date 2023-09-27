from __future__ import annotations


def test_no_settings(settings, client):
    response = client.get("/")
    assert "reporting-endpoints" not in response.headers
    assert "report-to" not in response.headers


def test_reporting_endpoints_string(settings, client):
    settings.REPORTING_ENDPOINTS = 'endpoint1="/_/csp-reports/"'
    response = client.get("/")
    assert response.headers["reporting-endpoints"] == 'endpoint1="/_/csp-reports/"'
    assert "report-to" not in response.headers


def test_reporting_endpoints_dict(settings, client):
    settings.REPORTING_ENDPOINTS = {
        "endpoint1": "/_/csp-reports/",
        "endpoint2": "/another/endpoint",
    }
    response = client.get("/")
    assert (
        response.headers["reporting-endpoints"]
        == 'endpoint1="/_/csp-reports/",endpoint2="/another/endpoint"'
    )
    assert "report-to" not in response.headers


def test_report_to_endpoints_string(settings, client):
    settings.REPORT_TO_ENDPOINTS = '{"group": "endpoint1", "max_age": 10886400, "endpoints": [{"url": "/_/csp-reports/"}]}'  # noqa: E501
    response = client.get("/")
    assert "reporting-endpoints" not in response.headers
    assert response.headers["report-to"] == settings.REPORT_TO_ENDPOINTS


def test_report_to_endpoints_dict(settings, client):
    settings.REPORT_TO_ENDPOINTS = {
        "group": "endpoint1",
        "max_age": 10886400,
        "endpoints": [{"url": "/_/csp-reports/"}],
    }
    response = client.get("/")
    assert "reporting-endpoints" not in response.headers
    assert (
        response.headers["report-to"]
        == '{"group": "endpoint1", "max_age": 10886400, "endpoints": [{"url": "/_/csp-reports/"}]}'  # noqa: E501
    )


def test_report_to_endpoints_list(settings, client):
    settings.REPORT_TO_ENDPOINTS = [
        {
            "group": "endpoint1",
            "max_age": 10886400,
            "endpoints": [{"url": "/_/csp-reports/"}],
        },
        {
            "group": "endpoint2",
            "max_age": 10886400,
            "endpoints": [{"url": "/another/endpoint"}],
        },
    ]
    response = client.get("/")
    assert "reporting-endpoints" not in response.headers
    assert (
        response.headers["report-to"]
        == '{"group": "endpoint1", "max_age": 10886400, "endpoints": [{"url": "/_/csp-reports/"}]},{"group": "endpoint2", "max_age": 10886400, "endpoints": [{"url": "/another/endpoint"}]}'  # noqa: E501
    )
