# from os.path import dirname, basename, isfile, join
# import glob
# modules = glob.glob(join(dirname(__file__), "*.py"))
# __all__ = [ f'.{basename(f)[:-3]}' for f in modules if isfile(f) and not f.endswith('__init__.py')]
# print(__all__)

# import os
# for module in os.listdir(os.path.dirname(__file__)):
#     if module == '__init__.py' or module[-3:] != '.py':
#         continue
#     __import__(module[:-3], locals(), globals())
# del module

from .api_attachment_models import *
from .api_models import *
from .authentication_models import *
from .mileage_models import *