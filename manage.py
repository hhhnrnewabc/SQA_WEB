#!/usr/bin/env python
import os
import sys

AWSTMPFILE = "onaws.tmp"

# check file is exist and not empty
if os.path.isfile(AWSTMPFILE) and os.stat(AWSTMPFILE)[6] != 0:
    with open(AWSTMPFILE) as readfile:
        ONAWS = eval(readfile.readline())
        print("ON TEST MODE")
else:
    print("ON AWS MODE")
    ONAWS = True


if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SQA_Project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
