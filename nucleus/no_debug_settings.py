import os
from .settings import *

# Override DEBUG to False for testing purposes, in general
# use the production config instead of this unless you want to
# test without MySQL or Redis.
DEBUG = False
