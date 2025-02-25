"""Attribute Mixin"""

class AttributeMixin():
    """Address elements and derived properties"""

    @classmethod
    @property
    def premises_attrs(cls):
        """Returns Paf premises elements"""
        return (
            'organisation_name', 'department_name',
                'sub_building_name', 'building_name', 'building_number',
                'po_box_number'
            )

    @classmethod
    @property
    def post_attrs(cls):
        """Returns Paf post elements"""
        return ('post_town', 'postcode')

    @classmethod
    @property
    def other_attrs(cls):
        """Returns Paf other elements"""
        return ('concatenation_indicator', 'udprn')

    @classmethod
    @property
    def attrs(cls):
        """Returns all Paf address elements"""
        return(
            cls.premises_attrs
                + cls.dependent_thoroughfare_attrs
                + cls.thoroughfare_attrs
                + cls.locality_attrs
                + cls.post_attrs
                + cls.other_attrs
            )

    def is_empty(self, attr):
        """Returns if attribute value is empty"""
        return getattr(self, attr, '') == ''
