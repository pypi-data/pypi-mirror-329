"""Splitting String Attributes"""

import re

class SplitMixin():
    """Methods to extract various parts of a attribute value"""

    @classmethod
    def __but_last_word(cls, string):
        """Returns all but last word of the string"""
        try:
            *first, _ = string.split()
            return ' '.join(first)
        except ValueError:
            return ''

    @classmethod
    def __last_word(cls, string):
        """Returns last word of the string"""
        try:
            *_, last = string.split()
            return last
        except ValueError:
            return string

    @classmethod
    def __leading_digits(cls, string):
        """Returns the leading digits from the string"""
        match = re.match(r'^\d+', string)
        if match:
            return int(match.group(0))
        return 0

    @classmethod
    def __after_leading_digits(cls, string):
        """Returns the characters after the leading digits from the string"""
        match = re.match(r'^\d+', string)
        if match:
            end_of_digits = match.end()
            return string[end_of_digits:]
        return ''

    def but_last_word(self, attr):
        """Returns all but last word of the attribute"""
        return self.__but_last_word(str(getattr(self, attr, '')))

    def last_word(self, attr):
        """Returns last word of the attribute"""
        return self.__last_word(str(getattr(self, attr, '')))

    def leading_digits(self, attr):
        """Returns the leading digits from the attribute"""
        return self.__leading_digits(str(getattr(self, attr, '')))

    def after_leading_digits(self, attr):
        """Returns the characters after the leading digits from the attribute"""
        return self.__after_leading_digits(str(getattr(self, attr, '')))
