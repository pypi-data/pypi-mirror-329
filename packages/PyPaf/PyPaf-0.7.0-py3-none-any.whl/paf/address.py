"""PAF Address"""

# Tried using dataclasses.dataclass(frozen=True) decorator for immutablity but did not work"""
from .initiator import attribute_init
from .attribute import AttributeMixin
from .immutable import ImmutableMixin
from .lineable import LineableMixin
from .thoroughfare_locality import ThoroughfareLocalityMixin
from .premises.premises import Premises

class Address(ImmutableMixin, AttributeMixin, ThoroughfareLocalityMixin, LineableMixin):
    """Main PAF Address class"""

    @attribute_init
    def __init__(self, *args):
        """Initialise Address elements"""
        object.__setattr__(self, 'premises', Premises(*args))

    def __repr__(self):
        """Return full representation of an Address"""
        args = {k: getattr(self, k) for k in list(self.attrs) if getattr(self, k, None)}
        return self.__class__.__name__ + '(' + str(args) + ')'

    def __str__(self):
        """Return Address as string representation"""
        line = ', '.join(self.lines)
        if self.is_empty('postcode'):
            return line
        return '. '.join([line] + [getattr(self, 'postcode')])

    def __iter__(self):
        """Return Address as iterable"""
        yield from list(self.lines)
        if not self.is_empty('postcode'):
            yield from list([getattr(self, 'postcode')])

    def as_str(self):
        """Return Address as string"""
        return str(self)

    def as_list(self):
        """Return Address as list of strings"""
        return list(self)

    def as_tuple(self):
        """Return Address as tuple of strings"""
        return tuple(self)

    def as_dict(self):
        """Return Address as dictionary of strings"""
        address = {}
        for counter, line in enumerate(getattr(self, 'optional_lines'), 1):
            address[f"line_{counter}"] = line
        if not self.is_empty('post_town'):
            address['post_town'] = getattr(self, 'post_town')
        if not self.is_empty('postcode'):
            address['postcode'] = getattr(self, 'postcode')
        return address
