"""Rule 5"""

from .premisable import PremisableMixin

class Rule101(PremisableMixin):
    """Rule 5 processing"""

    @property
    def rule_attrs(self):
        """Returns premises list"""
        if getattr(self, 'concatenation_indicator', '') == 'Y':
            return ('number_sub_name_and_thoroughfare_or_locality',)
        return ('sub_building_name', 'number_and_thoroughfare_or_locality')

    @property
    def includes_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return True
