.. _configuration-chapter:

======================================
Configuring django-reporting-endpoints
======================================

Reporting-API_ is a working draft specification. Different browsers have
different versions implemented. ``django-reporting-endpoints`` purpose was to
cover the minimum configuration required to get it going.

.. note:
   The chrome team's `announcement of Reporting API`__ has useful details on
   how to set up and debug reporting endpoints.


Policy Settings
===============

These settings affect ``Reporting-Endpoints`` and ``Report-To`` headers
respectively. They default to *empty* and are not sent, unless explicitly set in
the settings.

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


.. _Reporting-API: https://www.w3.org/TR/reporting-1/
.. _announcement of Reporting API: https://developer.chrome.com/articles/reporting-api/
