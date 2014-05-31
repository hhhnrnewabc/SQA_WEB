#!/usr/bin/env python
import os
import sys

AWSTMPFILE = "onaws.tmp"

# check file is exist and not empty
if os.path.isfile(AWSTMPFILE) and os.stat(AWSTMPFILE)[6] != 0:
    with open(AWSTMPFILE) as readfile:
        ONAWS = eval(readfile.readline())
else:
    ONAWS = True


if __name__ == "__main__":

    with open(AWSTMPFILE, 'w') as outfile:

        if sys.argv[1] == "travis-ci":
            outfile.write("False")
            sys.argv = [sys.argv[0]] + sys.argv[2:]
        else:
            outfile.write("True")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SQA_Project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
