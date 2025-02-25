"""Lineable Mixin"""

from itertools import chain

class LineableMixin():
    """Converts Paf address premises elements into list of lines"""

    @property
    def lines_attrs(self):
        """Returns premises line attributes"""
        return self.organisation_attrs + ('po_box',) + self.rule_attrs

    @property
    def lines(self):
        """Returns premises lines"""
        return self._lines(self.lines_attrs)

    @property
    def po_box(self):
        """Returns PO Box"""
        return '' if self.is_empty('po_box_number') else f"PO BOX {getattr(self, 'po_box_number')}"

    def _lines(self, attrs):
        """Returns list of premises lines from specified attributes"""
        lines = list(filter(None, [getattr(self, k, None) for k in attrs]))
        return list(chain(*[line if isinstance(line, list) else [line] for line in lines]))
