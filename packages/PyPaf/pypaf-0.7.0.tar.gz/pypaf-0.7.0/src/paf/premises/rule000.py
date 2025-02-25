"""Rule 1"""

from .premisable import PremisableMixin

class Rule000(PremisableMixin):
    """Rule 1 processing"""

    @property
    def rule_attrs(self):
        """Returns premises list"""
        return ()

    @property
    def includes_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return False

    @property
    def _premises_name(self):
        """Returns premises name"""
        if getattr(self, 'dependent_thoroughfare', '') != '':
            return getattr(self, 'dependent_thoroughfare', '')
        if getattr(self, 'organisation_name', '') != '':
            return getattr(self, 'organisation_name', '')
        if getattr(self, 'po_box', '') != '':
            return getattr(self, 'po_box', '')
        return super()._premises_name

    @property
    def _sub_premises_name(self):
        """Returns sub-premises name"""
        if getattr(self, 'dependent_thoroughfare', '') != '':
            if getattr(self, 'organisation_name', '') != '':
                return getattr(self, 'organisation_name', '')
            if getattr(self, 'po_box', '') != '':
                return getattr(self, 'po_box', '')
        return super()._sub_premises_name
