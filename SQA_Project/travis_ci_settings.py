from SQA_Project.settings import *

ONAWS = False 

if not ONAWS:
    from test.path import *
