"""Test Address Exception I formatting"""

import unittest
import paf

class TestExceptionI(unittest.TestCase):
    """Test Address Exception I"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'building_name': "1-2",
            'thoroughfare_name': "NURSERY",
            'thoroughfare_descriptor': "LANE",
            'dependent_locality': "PENN",
            'post_town': "HIGH WYCOMBE",
            'postcode': "HP10 8LS"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["1-2 NURSERY LANE", "PENN", "HIGH WYCOMBE", "HP10 8LS"]
        self.assertEqual(self.address.as_list(), address, "Incorrect Exception I list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "1-2 NURSERY LANE, PENN, HIGH WYCOMBE. HP10 8LS"
        self.assertEqual(self.address.as_str(), address, "Incorrect Exception I string format")

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = ("1-2 NURSERY LANE", "PENN", "HIGH WYCOMBE", "HP10 8LS")
        self.assertEqual(self.address.as_tuple(), address, "Incorrect Exception I tuple format")

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "1-2 NURSERY LANE",
            'line_2': "PENN",
            'post_town': "HIGH WYCOMBE",
            'postcode': "HP10 8LS"
            }
        self.assertEqual(self.address.as_dict(), address, "Incorrect Exception I dict format")

    def test_premises(self):
        """Test premises"""
        premises = {'premises_number': 1, 'premises_suffix': '-2'}
        self.assertEqual(self.address.premises(), premises, "Incorrect Exception I premises")

if __name__ == '__main__':
    unittest.main()
