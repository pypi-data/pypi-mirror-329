"""Premises Extender Mixin"""

import sys
from .rule000 import Rule000 # pylint: disable=unused-import
from .rule001 import Rule001 # pylint: disable=unused-import
from .rule010 import Rule010 # pylint: disable=unused-import
from .rule011 import Rule011 # pylint: disable=unused-import
from .rule101 import Rule101 # pylint: disable=unused-import
from .rule110 import Rule110 # pylint: disable=unused-import
from .rule111 import Rule111 # pylint: disable=unused-import

class ExtenderMixin():
    """Dynamic Premises processing"""

    @property
    def rule(self):
        """Returns premises rule class"""
        rule = ''.join(['0' if self.is_empty(k) else '1' for k in self.building_attrs])
        return getattr(sys.modules[__name__], 'Rule' + rule)

    def extend(self):
        """Dynamically extends instance with appropriate rule"""
        base_cls = self.__class__
        object.__setattr__(self, '__class__', type(base_cls.__name__, (base_cls, self.rule), {}))
