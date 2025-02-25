"""Initiator Decorator"""

import functools

def attribute_init(func):
    """Decorator to initiate an object based on a list of attributes"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        """Initiate properties from specified dict"""
        for key in list(getattr(self, 'attrs', [])):
            object.__setattr__(self, key, '')
        for key, val in args[0].items():
            if hasattr(self, key):
                object.__setattr__(self, key, str(val))
        return func(self, *args, **kwargs)

    return wrapper
