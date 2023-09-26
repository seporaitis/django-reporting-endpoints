#!/usr/bin/env python
from __future__ import annotations

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    sys.path.insert(0, "src")
    sys.path.insert(0, ".")
    from django.core.management import execute_from_command_line

    args = sys.argv + ["makemigrations", "reporting_endpoints"]
    execute_from_command_line(args)
