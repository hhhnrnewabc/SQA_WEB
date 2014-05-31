#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from server_mode import set_server_mode_test

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SQA_Project.settings")

if __name__ == "__main__":

    set_server_mode_test()

    from django.core.management import execute_from_command_line
    args = sys.argv
    args.insert(1, "test")
    execute_from_command_line(args)
