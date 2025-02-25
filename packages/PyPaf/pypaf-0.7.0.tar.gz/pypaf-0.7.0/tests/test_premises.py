"""Test Premises attributes"""

import unittest
import paf

class TestPremisesRule1(unittest.TestCase):
    """Test Premises Rule 1"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'organisation_name': "ACME LTD",
            'dependent_thoroughfare_name': "INDUSTRIAL",
            'dependent_thoroughfare_descriptor': "ESTATE",
            'thoroughfare_name': "RODING",
            'thoroughfare_descriptor': "ROAD",
            'post_town': "LONDON",
            'postcode': "E6 7HS"
            })

    def test_premises(self):
        """Test premises"""
        premises = {'premises_name': 'INDUSTRIAL ESTATE', 'sub_premises_name': 'ACME LTD'}
        self.assertEqual(
            self.address.premises(), premises, "Incorrect Rule 1 w/ Dependent Thoroughfare"
            )

class TestPremisesRule2(unittest.TestCase):
    """Test Premises Rule 2"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'building_number': "7",
            'dependent_thoroughfare_name': "SEASTONE",
            'dependent_thoroughfare_descriptor': "COURT",
            'thoroughfare_name': "STATION",
            'thoroughfare_descriptor': "LANE",
            'post_town': "HOLT",
            'postcode': "NR25 7HG"
            })

    def test_premises(self):
        """Test premises"""
        premises = {'premises_name': 'SEASTONE COURT', 'sub_premises_number': 7}
        self.assertEqual(
            self.address.premises(), premises, "Incorrect Rule 2 w/ Dependent Thoroughfare"
            )

class TestPremisesRule4(unittest.TestCase):
    """Test Premises Rule 2"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'building_name': "CARETAKERS FLAT",
            'building_number': "99",
            'dependent_thoroughfare_name': "SEASTONE",
            'dependent_thoroughfare_descriptor': "COURT",
            'thoroughfare_name': "STATION",
            'thoroughfare_descriptor': "AVENUE",
            'post_town': "HOLT",
            'postcode': "NR25 7HG"
            })

    def test_premises(self):
        """Test premises"""
        premises = {
            'premises_name': 'SEASTONE COURT',
            'sub_premises_number': 99,
            'sub_premises_name': 'CARETAKERS FLAT'
            }
        self.assertEqual(
            self.address.premises(), premises, "Incorrect Rule 4 w/ Dependent Thoroughfare"
            )

if __name__ == '__main__':
    unittest.main()
