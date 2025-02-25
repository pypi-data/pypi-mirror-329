"""Attribute Mixin"""

class AttributeMixin():
    """Premises elements and derived properties"""

    @classmethod
    @property
    def organisation_attrs(cls):
        """Returns Paf organisation elements"""
        return ('organisation_name', 'department_name')

    @classmethod
    @property
    def building_attrs(cls):
        """Returns Paf building elements"""
        return ('sub_building_name', 'building_name', 'building_number')

    @classmethod
    @property
    def other_attrs(cls):
        """Returns Paf other elements"""
        return ('po_box_number', 'concatenation_indicator')

    @classmethod
    @property
    def attrs(cls):
        """Returns all Paf premises elements"""
        return(
            cls.organisation_attrs
                + cls.building_attrs
                + cls.dependent_thoroughfare_attrs
                + cls.thoroughfare_attrs
                + cls.locality_attrs
                + cls.other_attrs
            )

    def is_empty(self, attr):
        """Returns if attribute value is empty"""
        return getattr(self, attr, '') == ''
