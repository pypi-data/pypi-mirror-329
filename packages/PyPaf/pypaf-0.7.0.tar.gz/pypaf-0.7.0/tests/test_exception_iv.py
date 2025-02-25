"""Test Address Exception IV formatting"""

import unittest
import paf

class TestExceptionIVUnit(unittest.TestCase):
    """Test Address Exception IV Unit"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'organisation_name': "THE TAMBOURINE WAREHOUSE",
            'building_name': "UNIT 1-3",
            'dependent_thoroughfare_name': "INDUSTRIAL",
            'dependent_thoroughfare_descriptor': "ESTATE",
            'thoroughfare_name': "TAME",
            'thoroughfare_descriptor': "ROAD",
            'post_town': "LONDON",
            'postcode': "E6 7HS"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = [
            "THE TAMBOURINE WAREHOUSE",
            "UNIT 1-3",
            "INDUSTRIAL ESTATE",
            "TAME ROAD",
            "LONDON",
            "E6 7HS"
            ]
        self.assertEqual(self.address.as_list(), address, "Incorrect Exception IV Unit list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "THE TAMBOURINE WAREHOUSE, UNIT 1-3, INDUSTRIAL ESTATE, TAME ROAD, LONDON. E6 7HS"
        self.assertEqual(
            self.address.as_str(), address, "Incorrect Exception IV Unit string format"
            )

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = (
            "THE TAMBOURINE WAREHOUSE",
            "UNIT 1-3",
            "INDUSTRIAL ESTATE",
            "TAME ROAD",
            "LONDON",
            "E6 7HS"
            )
        self.assertEqual(
            self.address.as_tuple(), address, "Incorrect Exception IV Unit tuple format"
            )

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "THE TAMBOURINE WAREHOUSE",
            'line_2': "UNIT 1-3",
            'line_3': "INDUSTRIAL ESTATE",
            'line_4': "TAME ROAD",
            'post_town': "LONDON",
            'postcode': "E6 7HS"
            }
        self.assertEqual(
            self.address.as_dict(), address, "Incorrect Exception IV Unit dict format"
            )

    def test_premises(self):
        """Test premises"""
        premises = {
            'premises_name': 'INDUSTRIAL ESTATE',
            'sub_premises_type': 'UNIT',
            'sub_premises_number': 1,
            'sub_premises_suffix': '-3'
            }
        self.assertEqual(self.address.premises(), premises, "Incorrect Exception IV Unit premises")

class TestExceptionIVStall(unittest.TestCase):
    """Test Address Exception IV Stall"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'organisation_name': "QUIRKY CANDLES LTD",
            'building_name': "STALL 4",
            'thoroughfare_name': "MARKET",
            'thoroughfare_descriptor': "SQUARE",
            'post_town': "LIVERPOOL",
            'postcode': "L8 1LH"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = [
            "QUIRKY CANDLES LTD",
            "STALL 4",
            "MARKET SQUARE",
            "LIVERPOOL",
            "L8 1LH"
            ]
        self.assertEqual(
            self.address.as_list(), address, "Incorrect Exception IV Stall list format"
            )

    def test_string(self):
        """Test conversion to a string"""
        address = "QUIRKY CANDLES LTD, STALL 4, MARKET SQUARE, LIVERPOOL. L8 1LH"
        self.assertEqual(
            self.address.as_str(), address, "Incorrect Exception IV Stall string format"
            )

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = (
            "QUIRKY CANDLES LTD",
            "STALL 4",
            "MARKET SQUARE",
            "LIVERPOOL",
            "L8 1LH"
            )
        self.assertEqual(
            self.address.as_tuple(), address, "Incorrect Exception IV Stall tuple format"
            )

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "QUIRKY CANDLES LTD",
            'line_2': "STALL 4",
            'line_3': "MARKET SQUARE",
            'post_town': "LIVERPOOL",
            'postcode': "L8 1LH"
            }
        self.assertEqual(
            self.address.as_dict(), address, "Incorrect Exception IV Stall dict format"
            )

    def test_premises(self):
        """Test premises"""
        premises = {'premises_type': 'STALL', 'premises_number': 4}
        self.assertEqual(self.address.premises(), premises, "Incorrect Exception IV Stall premises")

class TestExceptionIVRearOf(unittest.TestCase):
    """Test Address Exception IV Rear Of"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'organisation_name': "FIONA'S FLOWERS",
            'building_name': "REAR OF 5A",
            'thoroughfare_name': "HIGH",
            'thoroughfare_descriptor': "STREET",
            'post_town': "GATESHEAD",
            'postcode': "NE8 1BH"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = [
            "FIONA'S FLOWERS",
            "REAR OF 5A",
            "HIGH STREET",
            "GATESHEAD",
            "NE8 1BH"
            ]
        self.assertEqual(
            self.address.as_list(), address, "Incorrect Exception IV RearOf list format"
            )

    def test_string(self):
        """Test conversion to a string"""
        address = "FIONA'S FLOWERS, REAR OF 5A, HIGH STREET, GATESHEAD. NE8 1BH"
        self.assertEqual(
            self.address.as_str(), address, "Incorrect Exception IV RearOf string format"
            )

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = (
            "FIONA'S FLOWERS",
            "REAR OF 5A",
            "HIGH STREET",
            "GATESHEAD",
            "NE8 1BH"
            )
        self.assertEqual(
            self.address.as_tuple(), address, "Incorrect Exception IV RearOf tuple format"
            )

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "FIONA'S FLOWERS",
            'line_2': "REAR OF 5A",
            'line_3': "HIGH STREET",
            'post_town': "GATESHEAD",
            'postcode': "NE8 1BH"
            }
        self.assertEqual(
            self.address.as_dict(), address, "Incorrect Exception IV RearOf dict format"
            )

    def test_premises(self):
        """Test premises"""
        premises = {'premises_type': 'REAR OF', 'premises_number': 5, 'premises_suffix': 'A'}
        self.assertEqual(
            self.address.premises(), premises, "Incorrect Exception IV RearOf premises"
            )

class TestExceptionIVBlock(unittest.TestCase):
    """Test Address Exception IV BLock"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'building_name': "BLOCK B",
            'thoroughfare_name': "WELLESLEY",
            'thoroughfare_descriptor': "ROAD",
            'post_town': "CROYDON",
            'postcode': "CR9 1AT"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = [
            "BLOCK B",
            "WELLESLEY ROAD",
            "CROYDON",
            "CR9 1AT"
            ]
        self.assertEqual(
            self.address.as_list(), address, "Incorrect Exception IV Block list format"
            )

    def test_string(self):
        """Test conversion to a string"""
        address = "BLOCK B, WELLESLEY ROAD, CROYDON. CR9 1AT"
        self.assertEqual(
            self.address.as_str(), address, "Incorrect Exception IV Block string format"
            )

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = (
            "BLOCK B",
            "WELLESLEY ROAD",
            "CROYDON",
            "CR9 1AT"
            )
        self.assertEqual(
            self.address.as_tuple(), address, "Incorrect Exception IV Block tuple format"
            )

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "BLOCK B",
            'line_2': "WELLESLEY ROAD",
            'post_town': "CROYDON",
            'postcode': "CR9 1AT"
            }
        self.assertEqual(
            self.address.as_dict(), address, "Incorrect Exception IV Block dict format"
            )

    def test_premises(self):
        """Test premises"""
        premises = {'premises_type': 'BLOCK', 'premises_suffix': 'B'}
        self.assertEqual(self.address.premises(), premises, "Incorrect Exception IV Block premises")

if __name__ == '__main__':
    unittest.main()
