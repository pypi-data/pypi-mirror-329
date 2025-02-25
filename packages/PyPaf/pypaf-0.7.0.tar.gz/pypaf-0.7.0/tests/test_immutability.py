"""Test Immutability"""

import unittest
from dataclasses import FrozenInstanceError
import paf

class TestImmutability(unittest.TestCase):
    """Test Immutable"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'building_number': "16",
            'thoroughfare_name': "VIXEN",
            'thoroughfare_descriptor': "ROAD",
            'post_town': "BRADOCK",
            'postcode': "KT6 5BT"
            })

    def test_assignment(self):
        """Test setting attribute by direct assignment"""
        with self.assertRaises(FrozenInstanceError):
            self.address.building_name = "THE HOUSE"

    def test_setattr(self):
        """Test setting new attribute"""
        self.assertRaises(FrozenInstanceError, setattr, self.address, 'building_name', "THE HOUSE")

    def test_resetattr(self):
        """Test re-setting existing attribute"""
        self.assertRaises(FrozenInstanceError, setattr, self.address, 'building_number', "20")

    def test_delattr(self):
        """Test deleting attribute"""
        self.assertRaises(FrozenInstanceError, delattr, self.address, 'post_town')

if __name__ == '__main__':
    unittest.main()
