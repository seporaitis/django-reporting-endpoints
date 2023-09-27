.. _configuration-chapter:

======================================
Configuring django-reporting-endpoints
======================================

Reporting-API_ is a working draft specification. Different browsers have
different versions implemented. ``django-reporting-endpoints`` purpose was to
cover the minimum configuration required to get it going.

.. note::
   The chrome team's `announcement of Reporting API`_ has useful details on
   how to set up and debug reporting endpoints.


Policy Settings
===============

These settings affect ``Reporting-Endpoints`` and ``Report-To`` headers
respectively. They default to *empty* and are not sent, unless explicitly set in
the settings.

.. note::
   At the time of writing, reporting endpoints feature is available on Chromium
   based browsers only (e.g. Google Chrome). If you want to support multiple browsers,
   the recommendation is to configure both options.


``REPORTING_ENDPOINTS``
    Set it to a concrete string
    ``endpoint1-name="https://example.com/reports",endpoint2-name="/local/reports"``,
    the ``"`` (double-quotes) are significant. Alternatively, use a ``dict``:

    .. code-block:: python

       REPORTING_ENDPOINTS = {
           "endpoint1-name": "https://example.com/reports",
           "endpoint2-name": "/local/reports",
       }

    With the above example, you could use `endpoint1-name` and `endpoint2-name`
    in your `report-to` directives.

``REPORT_TO_ENDPOINTS``
    This configuration option can take a string, a dict, or a list. The general
    format of a report-to endpoint group is the following:

    .. code-block:: javascript

       {
           "group": "csp-violations",
           "max_age": 86400,
           "endpoints": [
              {"url": "https://example.com/reports"},
              {"url": "/local/reports"},
           ]
       }

    To set multiple groups, you can use a ``list``:

    .. code-block:: python

       REPORT_TO_ENDPOINTS = [
        {
            "group": "csp-violations",
            "max_age": 86400,
            "endpoints": [
              {"url": "/local/reports"},
            ]
        },
        {
            "group": "external-reporting",
            "max_age": 86400,
            "endpoints": [
              {"url": "https://example.com/reports"},
            ]
        },
       ]

    Alternatively, if you have just a single group, you can pass a single
    ``dict`` on its own. The configuration option can take a string value - the
    serialized value of the header.

    With the above example configuration options set, you could use
    `csp-violations` and `external-reporting` in your Content Security Policy
    `report-to` directives.


.. _Reporting-API: https://www.w3.org/TR/reporting-1/
.. _announcement of Reporting API: https://developer.chrome.com/articles/reporting-api/
