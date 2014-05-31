#!/usr/bin/env python
import os
import sys

from server_mode import get_server_mode

ONAWS = get_server_mode()


if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SQA_Project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
