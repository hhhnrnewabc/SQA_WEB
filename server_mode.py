#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

AWSTMPFILE = "onaws.tmp"


def get_server_mode():
    # check file is exist and not empty
    if os.path.isfile(AWSTMPFILE) and os.stat(AWSTMPFILE)[6] != 0:
        with open(AWSTMPFILE) as readfile:
            ONAWS = eval(readfile.readline())
            if ONAWS:
                print("ON AWS MODE")
            else:
                print("ON TEST MODE")
    else:
        print("ON AWS MODE")
        ONAWS = True

    return ONAWS


def set_server_mode_test():
    with open(AWSTMPFILE, 'w') as outfile:
        print("SET TO TEST MODE")
        outfile.write("False")


def set_server_mode_aws():
    with open(AWSTMPFILE, 'w') as outfile:
        print("SET TO AWS MODE")
        outfile.write("True")


if __name__ == '__main__':
    set_server_mode_aws()
