"""Immutable Mixin"""

from dataclasses import FrozenInstanceError

class ImmutableMixin():
    """Prevent manipulation of object attributes"""

    def __setattr__(self, *_):
        raise FrozenInstanceError

    def __delattr__(self, *_):
        raise FrozenInstanceError
