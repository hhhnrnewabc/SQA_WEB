#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from manage import AWSTMPFILE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SQA_Project.settings")

if __name__ == "__main__":

    with open(AWSTMPFILE, 'w') as outfile:
        print("START TEST MODE")
        outfile.write("False")

    from django.core.management import execute_from_command_line
    args = sys.argv
    args.insert(1, "test")
    execute_from_command_line(args)
