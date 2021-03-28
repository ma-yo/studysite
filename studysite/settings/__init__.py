# settings/__init__.py

try:
    from .production import *
except:
    pass

try:
    from .local import *
except:
    pass