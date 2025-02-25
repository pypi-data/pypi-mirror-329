"""Test Address Rule 1 formatting"""

import unittest
import paf

class TestRule1(unittest.TestCase):
    """Test Address Rule 1"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'organisation_name': "LEDA ENGINEERING LTD",
            'dependent_locality': "APPLEFORD",
            'post_town': "ABINGDON",
            'postcode': "OX14 4PG"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["LEDA ENGINEERING LTD", "APPLEFORD", "ABINGDON", "OX14 4PG"]
        self.assertEqual(self.address.as_list(), address, "Incorrect Rule 1 list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "LEDA ENGINEERING LTD, APPLEFORD, ABINGDON. OX14 4PG"
        self.assertEqual(self.address.as_str(), address, "Incorrect Rule 1 string format")

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = ("LEDA ENGINEERING LTD", "APPLEFORD", "ABINGDON", "OX14 4PG")
        self.assertEqual(self.address.as_tuple(), address, "Incorrect Rule 1 tuple format")

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "LEDA ENGINEERING LTD",
            'line_2': "APPLEFORD",
            'post_town': "ABINGDON",
            'postcode': "OX14 4PG"
            }
        self.assertEqual(self.address.as_dict(), address, "Incorrect Rule 1 dict format")

    def test_premises(self):
        """Test premises"""
        premises = {'premises_name': 'LEDA ENGINEERING LTD'}
        self.assertEqual(self.address.premises(), premises, "Incorrect Rule 1 premises")

if __name__ == '__main__':
    unittest.main()
