"""Dependent Premisable Mixin"""

from .premisable import PremisableMixin

class DependentPremisableMixin(PremisableMixin):
    """Returns the values for the premises properties"""

    @property
    def _premises_number(self):
        """Returns premises number"""
        if getattr(self, 'dependent_thoroughfare', '') != '':
            return ''
        return super()._premises_number

    @property
    def _premises_name(self):
        """Returns premises name"""
        if getattr(self, 'dependent_thoroughfare', '') != '':
            return getattr(self, 'dependent_thoroughfare', '')
        return super()._premises_name

    @property
    def _sub_premises_number(self):
        """Returns sub-premises number"""
        if getattr(self, 'dependent_thoroughfare', '') != '':
            return super()._premises_number
        return super()._sub_premises_number

    @property
    def _sub_premises_name(self):
        """Returns sub-premises name"""
        if getattr(self, 'dependent_thoroughfare', '') != '':
            return super()._premises_name
        return super()._sub_premises_name
