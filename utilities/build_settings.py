from settings import *
import os
try:
    from settings import PROJECT_DIR
except ImportError:
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

try:
    from settings import PROJECT_PATH_JOIN
except ImportError:
    PROJECT_PATH_JOIN = lambda a, *p: os.path.join(PROJECT_DIR, a, *p)

# This file is use for point collectstatic to
#
# current--
#         |-- service
#         |-- static *
#         |-- virtuelenv

STATIC_ROOT = PROJECT_PATH_JOIN('../static')
