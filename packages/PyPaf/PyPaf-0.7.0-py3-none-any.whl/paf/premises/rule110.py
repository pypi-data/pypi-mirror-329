"""Rule 6"""

from .premisable import PremisableMixin

class Rule110(PremisableMixin):
    """Rule 6 processing"""

    @property
    def rule_attrs(self):
        """Returns premises list"""
        if self.is_exception('sub_building_name'):
            return('sub_name_and_name',)
        if self.is_exception('building_name'):
            return('sub_building_name', 'name_and_thoroughfare_or_locality')
        return ('sub_building_name', 'building_name')

    @property
    def includes_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return (not self.is_exception('sub_building_name')) and self.is_exception('building_name')
