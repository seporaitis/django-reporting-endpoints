Installation
============

Requirements
------------

Python 3.8 to 3.12 supported.

Django 3.2 to 5.0 supported.

Step (5) below assumes that you are using `django-csp <https://django-csp.readthedocs.io/en/latest/>`_.

Installation
------------

1. Install with **pip**:

   .. code-block:: sh

       python -m pip install django-reporting-endpoints

2. Add django-reporting-endpoints to your ``INSTALLED_APPS``:

   .. code-block:: python

       INSTALLED_APPS = [
           ...,
           "reporting_endpoints",
           ...,
       ]

3. Configure your ``REPORTING_ENDPOINTS``:

   .. code-block:: python

       REPORTING_ENDPOINTS = {
           "csp-violations": "/_/csp-reports/",
       }

4. Add the middleware:

   .. code-block:: python

       MIDDLEWARE = [
           ...,
           "reporting_endpoints.middleware.ReportingEndpointsMiddleware",
           ...,
       ]

4. Add the view to your urlconfig:

   .. code-block:: python

       urlpatterns = [
           ...,
           path(
               "_/csp-reports/", reporting_endpoint, kwargs={"endpoint_name": "csp-endpoint"}
           ),
       ]

5. Configure your ``report-to`` directives for the packages you use. For example, if you use ``django-csp``:

   .. code-block:: python

       CSP_REPORT_TO = "csp-violations"
