"""Test Address Exception III formatting"""

import unittest
import paf

class TestExceptionIII(unittest.TestCase):
    """Test Address Exception III"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'building_name': "K",
            'thoroughfare_name': "PORTLAND",
            'thoroughfare_descriptor': "ROAD",
            'post_town': "DORKING",
            'postcode': "RH4 1EW"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["K PORTLAND ROAD", "DORKING", "RH4 1EW"]
        self.assertEqual(self.address.as_list(), address, "Incorrect Exception III list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "K PORTLAND ROAD, DORKING. RH4 1EW"
        self.assertEqual(self.address.as_str(), address, "Incorrect Exception III string format")

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = ("K PORTLAND ROAD", "DORKING", "RH4 1EW")
        self.assertEqual(self.address.as_tuple(), address, "Incorrect Exception III tuple format")

    def test_dict(self):
        """Test conversion to a dict"""
        address = {'line_1': "K PORTLAND ROAD", 'post_town': "DORKING", 'postcode': "RH4 1EW"}
        self.assertEqual(self.address.as_dict(), address, "Incorrect Exception III dict format")

    def test_premises(self):
        """Test premises"""
        premises = {'premises_name': 'K'}
        self.assertEqual(self.address.premises(), premises, "Incorrect Exception III premises")

if __name__ == '__main__':
    unittest.main()
