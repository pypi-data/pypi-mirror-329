"""Address Premises"""

from ..initiator import attribute_init
from ..immutable import ImmutableMixin
from ..thoroughfare_locality import ThoroughfareLocalityMixin
from .attribute import AttributeMixin
from .extender import ExtenderMixin
from .lineable import LineableMixin
from .split import SplitMixin

class Premises(
    ImmutableMixin, ExtenderMixin, AttributeMixin,
        ThoroughfareLocalityMixin, LineableMixin, SplitMixin
    ):
    """PAF Address Premises class"""

    @attribute_init
    def __init__(self, *args): # pylint: disable=unused-argument
        """Initialise Premises elements"""
        self.extend()

    def __repr__(self):
        """Return full representation of a Premises"""
        args = {k: getattr(self, k) for k in list(self.attrs) if getattr(self, k, None)}
        return self.__class__.__name__ + '(' + str(args) + ')'

    def __str__(self):
        """Return Premises as string representation"""
        return ', '.join(self.lines)

    def __iter__(self):
        """Return Premises as iterable"""
        yield from list(self.lines)

    def __call__(self):
        """Return Premises as dictionary"""
        return self.as_premisable() # pylint: disable=no-member

    @property
    def building_number_and_sub_building_name(self):
        """Returns building number and sub-building name"""
        return self._concatenate(('building_number', 'sub_building_name'), '')

    @property
    def name_and_thoroughfare_or_locality(self):
        """Returns building number and first thoroughfare or locality"""
        return self._concatenate(('building_name', 'first_thoroughfare_or_locality'))

    @property
    def name_last_word_and_thoroughfare_or_locality(self):
        """Returns last word of building name and first thoroughfare or locality"""
        return self._concatenate(('building_name_last_word', 'first_thoroughfare_or_locality'))

    @property
    def number_and_thoroughfare_or_locality(self):
        """Returns building number and first thoroughfare or locality"""
        return self._concatenate(('building_number', 'first_thoroughfare_or_locality'))
    @property
    def number_sub_name_and_thoroughfare_or_locality(self):
        """Returns building number, sub-building name and first thoroughfare or locality"""
        return self._concatenate(
            ('building_number_and_sub_building_name', 'first_thoroughfare_or_locality')
            )

    @property
    def sub_name_and_name(self):
        """Returns sub-building name and building name"""
        return self._concatenate(('sub_building_name', 'building_name'))

    @property
    def sub_name_comma_name(self):
        """Returns sub-building name and building name concatenated with a comma"""
        return self._concatenate(('sub_building_name', 'building_name'), ', ')

    @property
    def building_name_but_last_word(self):
        """Returns all but last word of the building name"""
        return self.but_last_word('building_name')

    @property
    def building_name_last_word(self):
        """Returns last word of the building name"""
        return self.last_word('building_name')

    @property
    def sub_building_name_but_last_word(self):
        """Returns all but last word of the sub-building name"""
        return self.but_last_word('sub_building_name')

    @property
    def sub_building_name_last_word(self):
        """Returns last word of the sub-building name"""
        return self.last_word('sub_building_name')

    def _concatenate(self, keys, concatenator=' '):
        """Returns specified attributes concatenated with a specified separator"""
        return concatenator.join(filter(None, [getattr(self, k, None) for k in keys]))
