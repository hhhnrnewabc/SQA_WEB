#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    if sys.argv[1] == "travis-ci":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SQA_Project.travis_ci_settings")
        sys.argv = [sys.argv[0]] + sys.argv[2:]
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SQA_Project.aws_settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
