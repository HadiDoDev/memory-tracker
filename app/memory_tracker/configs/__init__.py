import os

from ..constants import TRUE_VALUES

PRODUCTION = os.getenv('PRODUCTION_MODE')
if PRODUCTION in TRUE_VALUES:
    from .production import *
else:
    from .development import *
