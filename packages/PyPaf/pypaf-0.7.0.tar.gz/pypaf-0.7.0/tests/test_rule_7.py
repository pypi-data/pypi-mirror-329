"""Test Address Rule 7 formatting"""

import unittest
import paf

class TestRule7WithZeroBuildingNumber(unittest.TestCase):
    """Test Address Rule 7 with a 0 Building Number"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'sub_building_name': "FLAT 1",
            'building_name': "HOLLY HOUSE",
            'building_number': "0",
            'thoroughfare_name': "OAK",
            'thoroughfare_descriptor': "AVENUE",
            'dependent_locality': "BIDDENDEN",
            'post_town': "ASHFORD",
            'postcode': "TN27 8BT"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["FLAT 1, HOLLY HOUSE", "OAK AVENUE", "BIDDENDEN", "ASHFORD", "TN27 8BT"]
        self.assertEqual(
            self.address.as_list(), address, "Incorrect Rule 7 with 0 building number list format"
            )

    def test_string(self):
        """Test conversion to a string"""
        address = "FLAT 1, HOLLY HOUSE, OAK AVENUE, BIDDENDEN, ASHFORD. TN27 8BT"
        self.assertEqual(
            self.address.as_str(), address, "Incorrect Rule 7 with 0 building number string format"
            )

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = ("FLAT 1, HOLLY HOUSE", "OAK AVENUE", "BIDDENDEN", "ASHFORD", "TN27 8BT")
        self.assertEqual(
            self.address.as_tuple(), address, "Incorrect Rule 7 with 0 building number tuple format"
            )

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "FLAT 1, HOLLY HOUSE",
            'line_2': "OAK AVENUE",
            'line_3': "BIDDENDEN",
            'post_town': "ASHFORD",
            'postcode': "TN27 8BT"
            }
        self.assertEqual(
            self.address.as_dict(), address, "Incorrect Rule 7 with 0 building number dict format"
            )

    def test_premises(self):
        """Test premises"""
        premises = {
            'premises_name': 'HOLLY HOUSE',
            'sub_premises_type': 'FLAT',
            'sub_premises_number': 1
            }
        self.assertEqual(
            self.address.premises(), premises, "Incorrect Rule 7 with 0 building number premises"
            )

class TestRule7WithSubBuildingName(unittest.TestCase):
    """Test Address Rule 7 with Sub-Building Name Exception"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'sub_building_name': "2B",
            'building_name': "THE TOWER",
            'building_number': "27",
            'thoroughfare_name': "JOHN",
            'thoroughfare_descriptor': "STREET",
            'post_town': "WINCHESTER",
            'postcode': "SO23 9AP"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["2B THE TOWER", "27 JOHN STREET", "WINCHESTER", "SO23 9AP"]
        self.assertEqual(
            self.address.as_list(), address, "Incorrect Rule 7 with sub-building list format"
            )

    def test_string(self):
        """Test conversion to a string"""
        address = "2B THE TOWER, 27 JOHN STREET, WINCHESTER. SO23 9AP"
        self.assertEqual(
            self.address.as_str(), address, "Incorrect Rule 7 with sub-building string format"
            )

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = ("2B THE TOWER", "27 JOHN STREET", "WINCHESTER", "SO23 9AP")
        self.assertEqual(
            self.address.as_tuple(), address, "Incorrect Rule 7 with sub-building tuple format"
            )

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "2B THE TOWER",
            'line_2': "27 JOHN STREET",
            'post_town': "WINCHESTER",
            'postcode': "SO23 9AP"
            }
        self.assertEqual(
            self.address.as_dict(), address, "Incorrect Rule 7 with sub-building dict format"
            )

    def test_premises(self):
        """Test premises"""
        premises = {
            'premises_number': 27,
            'premises_name': 'THE TOWER',
            'sub_premises_number': 2,
            'sub_premises_suffix': 'B'
            }
        self.assertEqual(
            self.address.premises(), premises, "Incorrect Rule 7 with sub-building premises"
            )

class TestRule7(unittest.TestCase):
    """Test Address Rule 7 without Exception"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'sub_building_name': "BASEMENT FLAT",
            'building_name': "VICTORIA HOUSE",
            'building_number': "15",
            'thoroughfare_name': "THE",
            'thoroughfare_descriptor': "STREET",
            'post_town': "CORYTON",
            'postcode': "BP23 6AA"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["BASEMENT FLAT", "VICTORIA HOUSE", "15 THE STREET", "CORYTON", "BP23 6AA"]
        self.assertEqual(self.address.as_list(), address, "Incorrect Rule 7 list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "BASEMENT FLAT, VICTORIA HOUSE, 15 THE STREET, CORYTON. BP23 6AA"
        self.assertEqual(self.address.as_str(), address, "Incorrect Rule 7 string format")

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = ("BASEMENT FLAT", "VICTORIA HOUSE", "15 THE STREET", "CORYTON", "BP23 6AA")
        self.assertEqual(self.address.as_tuple(), address, "Incorrect Rule 7 tuple format")

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "BASEMENT FLAT",
            'line_2': "VICTORIA HOUSE",
            'line_3': "15 THE STREET",
            'post_town': "CORYTON",
            'postcode': "BP23 6AA"
            }
        self.assertEqual(self.address.as_dict(), address, "Incorrect Rule 7 dict format")

    def test_premises(self):
        """Test premises"""
        premises = {
            'premises_number': 15,
            'premises_name': 'VICTORIA HOUSE',
            'sub_premises_name': 'BASEMENT FLAT'
            }
        self.assertEqual(self.address.premises(), premises, "Incorrect Rule 7 premises")

if __name__ == '__main__':
    unittest.main()
