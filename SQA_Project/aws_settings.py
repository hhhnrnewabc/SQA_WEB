from SQA_Project.settings import *

ONAWS = True

# import path for AWS EC2 SERVER
# . is point to WEB/
# path put in ../aws_path_fix.py
if ONAWS:
    import sys
    sys.path.insert(0, '..')
    from aws_path_fix import *
