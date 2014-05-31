#!/usr/bin/env python
import os
import sys

ONAWS = True

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SQA_Project.settings")

    if sys.argv[1] == "travis-ci":
        ONAWS = False
        sys.argv = [sys.argv[0]] + sys.argv[2:]


    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
