Example Project
===============

The django-reporting-endpoints repository contains an `example project <https://github.com/seporaitis/django-reporting-endpoints/tree/main/example>`__, demonstrating use of django-reporting-endpoints.

To run it locally:

1. You will need to install `ngrok <https://ngrok.com/>`_ or similar.

2. Checkout the source code & install dependencies

3. Run migrations and setup a Django superuser.

   .. code-block:: bash

       python manage.py migrate
       python manage.py createsuperuser

3. Run django server & proxy it via https.

   .. code-block:: bash

       python manage.py runserver
       ngrok http 8000

4. Open the https address that ngrok gives you.

   The homepage is designed to trigger CSP violations and report them.

5. Open Django admin on `127.0.0.1:8000 <http://127.0.0.1:8000/admin/>`_ and investigate the reports.
