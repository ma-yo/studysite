# settings/__init__.py

try:
    from .production import *
except:
    try:
        from .local import *
    except:
        pass