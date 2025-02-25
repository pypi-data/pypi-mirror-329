"""Lineable Mixin"""

from itertools import chain

class LineableMixin():
    """Converts Paf address elements into list of address lines"""

    @classmethod
    @property
    def optional_lines_attrs(cls):
        """Returns optional address line attributes"""
        return ('thoroughfares_and_localities',)

    @classmethod
    @property
    def lines_attrs(cls):
        """Returns optional address line attributes and post_town"""
        return cls.optional_lines_attrs + ('post_town',)

    @property
    def optional_lines(self):
        """Returns address lines, excluding post_town and postcode"""
        return self.premises.lines + self._lines(self.optional_lines_attrs)

    @property
    def lines(self):
        """Returns address lines, excluding postcode"""
        return self.premises.lines + self._lines(self.lines_attrs)

    def _lines(self, attrs):
        """Returns list of address lines from specified attributes"""
        lines = list(filter(None, [getattr(self, k, None) for k in attrs]))
        return list(chain(*[line if isinstance(line, list) else [line] for line in lines]))
