"""Rule 7"""

from .premisable import PremisableMixin

class Rule111(PremisableMixin):
    """Rule 7 processing"""

    @property
    def rule_attrs(self):
        """Returns premises list"""
        if self.is_zero('building_number'):
            return('sub_name_comma_name',)
        if self.is_exception('sub_building_name'):
            return('sub_name_and_name', 'number_and_thoroughfare_or_locality')
        return ('sub_building_name', 'building_name', 'number_and_thoroughfare_or_locality')

    @property
    def includes_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return not self.is_zero('building_number')

    def is_zero(self, attr):
        """Returns if attribute value is a 0"""
        return getattr(self, attr, '') == "0"
