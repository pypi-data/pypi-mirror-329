"""Rule 4"""

from .dependent_premisable import DependentPremisableMixin

class Rule011(DependentPremisableMixin):
    """Rule 4 processing"""

    @property
    def rule_attrs(self):
        """Returns premises list"""
        return ('building_name', 'number_and_thoroughfare_or_locality')

    @property
    def includes_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return True
