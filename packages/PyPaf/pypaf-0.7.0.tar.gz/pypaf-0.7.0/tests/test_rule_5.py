"""Test Address Rule 5 formatting"""

import unittest
import paf

class TestRule5(unittest.TestCase):
    """Test Address Rule 5"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'sub_building_name': "FLAT 1",
            'building_number': "12",
            'thoroughfare_name': "LIME TREE",
            'thoroughfare_descriptor': "AVENUE",
            'post_town': "BRISTOL",
            'postcode': "BS8 4AB"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["FLAT 1", "12 LIME TREE AVENUE", "BRISTOL", "BS8 4AB"]
        self.assertEqual(self.address.as_list(), address, "Incorrect Rule 5 list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "FLAT 1, 12 LIME TREE AVENUE, BRISTOL. BS8 4AB"
        self.assertEqual(self.address.as_str(), address, "Incorrect Rule 5 string format")

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = ("FLAT 1", "12 LIME TREE AVENUE", "BRISTOL", "BS8 4AB")
        self.assertEqual(self.address.as_tuple(), address, "Incorrect Rule 5 tuple format")

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "FLAT 1",
            'line_2': "12 LIME TREE AVENUE",
            'post_town': "BRISTOL",
            'postcode': "BS8 4AB"
            }
        self.assertEqual(self.address.as_dict(), address, "Incorrect Rule 5 dict format")

    def test_premises(self):
        """Test premises"""
        premises = {'premises_number': 12, 'sub_premises_type': 'FLAT', 'sub_premises_number': 1}
        self.assertEqual(self.address.premises(), premises, "Incorrect Rule 5 premises")

class TestRule5WithConcatenation(unittest.TestCase):
    """Test Address Rule 5 with Concatenation"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'sub_building_name': "A",
            'building_number': "12",
            'thoroughfare_name': "HIGH",
            'thoroughfare_descriptor': "STREET NORTH",
            'dependent_locality': "COOMBE BISSETT",
            'post_town': "SALISBURY",
            'postcode': "SP5 4NA",
            'concatenation_indicator': "Y"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["12A HIGH STREET NORTH", "COOMBE BISSETT", "SALISBURY", "SP5 4NA"]
        self.assertEqual(
            self.address.as_list(), address, "Incorrect Rule 5 with concatenate list format"
            )

    def test_string(self):
        """Test conversion to a string"""
        address = "12A HIGH STREET NORTH, COOMBE BISSETT, SALISBURY. SP5 4NA"
        self.assertEqual(
            self.address.as_str(), address, "Incorrect Rule 5 with concatenate string format"
            )

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = ("12A HIGH STREET NORTH", "COOMBE BISSETT", "SALISBURY", "SP5 4NA")
        self.assertEqual(
            self.address.as_tuple(), address, "Incorrect Rule 5 with concatenate tuple format"
            )

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "12A HIGH STREET NORTH",
            'line_2': "COOMBE BISSETT",
            'post_town': "SALISBURY",
            'postcode': "SP5 4NA"
            }
        self.assertEqual(
            self.address.as_dict(), address, "Incorrect Rule 5 with concatenate dict format"
            )

    def test_premises(self):
        """Test premises"""
        premises = {'premises_number' : 12, 'sub_premises_name': 'A'}
        self.assertEqual(
            self.address.premises(), premises, "Incorrect Rule 5 with concatenate premises"
            )

if __name__ == '__main__':
    unittest.main()
