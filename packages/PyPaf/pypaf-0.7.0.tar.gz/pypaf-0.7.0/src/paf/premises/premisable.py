"""Premisable Mixin"""

from .exception import ExceptionMixin

class PremisableMixin(ExceptionMixin):
    """Returns the values for the premises properties"""

    @classmethod
    @property
    def premises_attrs(cls):
        """Returns derived premises elements"""
        return (
            'premises_type', 'premises_number', 'premises_suffix', 'premises_name',
            'sub_premises_type', 'sub_premises_number', 'sub_premises_suffix', 'sub_premises_name'
            )

    @property
    def _premises_number(self):
        """Returns premises number"""
        if self.has_building_number:
            return self.building_number
        if self.is_exception('building_name') or self.is_split_exception('building_name'):
            return self.building_name_last_word
        return ''

    @property
    def _premises_name(self):
        """Returns premises name"""
        if self.has_building_number:
            return self.building_name
        if self.is_exception('building_name') or self.is_split_exception('building_name'):
            return self.building_name_but_last_word
        return self.building_name

    @property
    def _premises_name_last_word(self):
        """Returns last word of the premises name"""
        return self.last_word('_premises_name')

    @property
    def _sub_premises_number(self):
        """Returns sub-premises number"""
        if self.is_exception('sub_building_name'):
            return self.sub_building_name_last_word
        return ''

    @property
    def _sub_premises_name(self):
        """Returns sub-premises name"""
        if self.is_exception('sub_building_name'):
            return self.sub_building_name_but_last_word
        return self.sub_building_name

    @property
    def _sub_premises_name_last_word(self):
        """Returns last word of the sub-premises name"""
        return self.last_word('_sub_premises_name')

    @property
    def premises_type(self):
        """Returns premises type"""
        if self._premises_number != '':
            return ''
        if self.is_known_building_type('_premises_name'):
            return self.but_last_word('_premises_name')
        return ''

    @property
    def premises_number(self):
        """Returns premises number"""
        if self._premises_number != '':
            return self.leading_digits('_premises_number')
        if self.is_known_building_type('_premises_name'):
            return self.leading_digits('_premises_name_last_word')
        return 0

    @property
    def premises_suffix(self):
        """Returns premises suffix"""
        if self._premises_number != '':
            return self.after_leading_digits('_premises_number')
        if self.is_known_building_type('_premises_name'):
            if self.leading_digits('_premises_name_last_word') == 0:
                return self._premises_name_last_word
            return self.after_leading_digits('_premises_name_last_word')
        return ''

    @property
    def premises_name(self):
        """Returns premises name"""
        if self._premises_number != '':
            if self.leading_digits('_premises_number') == 0:
                return self._premises_number
            return self._premises_name
        if self.is_known_building_type('_premises_name'):
            return ''
        return self._premises_name

    @property
    def sub_premises_type(self):
        """Returns sub-premises type"""
        if self._sub_premises_number != '':
            return ''
        if self.is_known_sub_building_type('_sub_premises_name'):
            return self.but_last_word('_sub_premises_name')
        return ''

    @property
    def sub_premises_number(self):
        """Returns sub-premises number"""
        if self._sub_premises_number != '':
            return self.leading_digits('_sub_premises_number')
        if self.is_known_sub_building_type('_sub_premises_name'):
            return self.leading_digits('_sub_premises_name_last_word')
        return 0

    @property
    def sub_premises_suffix(self):
        """Returns sub-premises suffix"""
        if self._sub_premises_number != '':
            return self.after_leading_digits('_sub_premises_number')
        if self.is_known_sub_building_type('_sub_premises_name'):
            if self.leading_digits('_sub_premises_name_last_word') == 0:
                return self._sub_premises_name_last_word
            return self.after_leading_digits('_sub_premises_name_last_word')
        return ''

    @property
    def sub_premises_name(self):
        """Returns sub-premises name"""
        if self._sub_premises_number != '':
            if self.leading_digits('_sub_premises_number') == 0:
                return self._sub_premises_number
            return self._sub_premises_name
        if self.is_known_sub_building_type('_sub_premises_name'):
            return ''
        return self._sub_premises_name

    @property
    def has_building_number(self):
        """Returns if address has a populated building number"""
        return self.building_number not in ('', '0')

    def as_premisable(self):
        """Return Premisable as dictionary"""
        return {
            attr: getattr(self, attr) for attr in self.premises_attrs
            if getattr(self, attr, None) and getattr(self, attr) != 0
            }
