"""Rule 3"""

from .dependent_premisable import DependentPremisableMixin

class Rule010(DependentPremisableMixin):
    """Rule 3 processing"""

    @property
    def rule_attrs(self):
        """Returns premises list"""
        if self.is_exception('building_name'):
            return ('name_and_thoroughfare_or_locality',)
        if self.is_split_exception('building_name'):
            return ('building_name_but_last_word', 'name_last_word_and_thoroughfare_or_locality')
        return ('building_name',)

    @property
    def includes_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return self.is_exception('building_name') or self.is_split_exception('building_name')
