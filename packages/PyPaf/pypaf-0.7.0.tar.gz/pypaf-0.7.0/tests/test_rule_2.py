"""Test Address Rule 2 formatting"""

import unittest
import paf

class TestRule2(unittest.TestCase):
    """Test Address Rule 2"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'building_number': "1",
            'thoroughfare_name': "ACACIA",
            'thoroughfare_descriptor': "AVENUE",
            'post_town': "ABINGDON",
            'postcode': "OX14 4PG"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["1 ACACIA AVENUE", "ABINGDON", "OX14 4PG"]
        self.assertEqual(self.address.as_list(), address, "Incorrect Rule 2 list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "1 ACACIA AVENUE, ABINGDON. OX14 4PG"
        self.assertEqual(self.address.as_str(), address, "Incorrect Rule 2 string format")

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = ("1 ACACIA AVENUE", "ABINGDON", "OX14 4PG")
        self.assertEqual(self.address.as_tuple(), address, "Incorrect Rule 2 tuple format")

    def test_dict(self):
        """Test conversion to a dict"""
        address = {'line_1': "1 ACACIA AVENUE", 'post_town': "ABINGDON", 'postcode': "OX14 4PG"}
        self.assertEqual(self.address.as_dict(), address, "Incorrect Rule 2 dict format")

    def test_premises(self):
        """Test premises"""
        premises = {'premises_number': 1}
        self.assertEqual(self.address.premises(), premises, "Incorrect empty premises")

if __name__ == '__main__':
    unittest.main()
