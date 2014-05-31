#!/usr/bin/env python
import os
import sys

with open("SQA_Project/onaws.pid") as readfile:
    ONAWS = eval(readfile.readline())


if __name__ == "__main__":

    with open("SQA_Project/onaws.pid", 'w') as outfile:

        if sys.argv[1] == "travis-ci":
            outfile.write("False")
            sys.argv = [sys.argv[0]] + sys.argv[2:]
        else:
            outfile.write("True")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SQA_Project.settings")


    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
