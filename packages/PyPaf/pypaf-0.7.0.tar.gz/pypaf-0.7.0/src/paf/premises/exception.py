"""Exceptions"""

import re
from .building_type import BuildingTypeMixin
from .split import SplitMixin

class ExceptionMixin(BuildingTypeMixin, SplitMixin):
    """Exceptions"""

    @classmethod
    def __is_exception_i(cls, val):
        """Returns if first and last characters are numeric"""
        return re.fullmatch(r'^[\d](?:.*[\d])?$', val)

    @classmethod
    def __is_exception_ii(cls, val):
        """Returns if first and penultimate characters are numeric, and last is alphabetic"""
        return re.fullmatch(r'^([\d][a-zA-Z]|[\d].*?[\d][a-zA-Z])$', val)

    @classmethod
    def __is_exception_iii(cls, val):
        """Returns if single non-whitespace character"""
        return re.fullmatch(r'^[^ \t\r\n\v\f]$', val)

    @classmethod
    def __is_exception(cls, val):
        """Returns if value is an exception"""
        return (
            cls.__is_exception_i(val)
                or cls.__is_exception_ii(val)
                or cls.__is_exception_iii(val)
            )

    def __is_exception_iv(self, attr):  # pylint: disable=unused-argument
        """Returns if value starts with a known building type
           and ends with numeric range or numeric alpha suffix"""
        # Do not include suffix check as does not account for values such as BLOCK B
        return self.is_known_building_type(attr)
        # and re.match(r'^\d', splitstring.last_word(getattr(self, attr, None)))

    def is_exception(self, attr):
        """Returns if attribute is an exception"""
        return self.__is_exception(getattr(self, attr, None))

    def is_split_exception(self, attr):
        """Returns if attribute should be split"""
        return (
            self.__is_exception(self.last_word(attr))
                and not self.last_word(attr).isdigit()
                and not self.__is_exception_iv(attr)
            )
