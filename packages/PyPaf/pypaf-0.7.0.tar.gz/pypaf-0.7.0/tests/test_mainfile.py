"""Test Address Mainfile formatting"""

import unittest
import paf

class TestMainfile(unittest.TestCase):
    """Test Address Mainfile"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({
            'organisation_name': "SOUTH LANARKSHIRE COUNCIL",
            'department_name': "HEAD START",
            'sub_building_name': "UNIT 1",
            'building_name': "BLOCK 3",
            'thoroughfare_name': "THIRD",
            'thoroughfare_descriptor': "ROAD",
            'double_dependent_locality': "BLANTYRE INDUSTRIAL ESTATE",
            'dependent_locality': "BLANTYRE",
            'post_town': "GLASGOW",
            'postcode': "G72 0UP"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = [
            "SOUTH LANARKSHIRE COUNCIL",
            "HEAD START",
            "UNIT 1",
            "BLOCK 3",
            "THIRD ROAD",
            "BLANTYRE INDUSTRIAL ESTATE",
            "BLANTYRE",
            "GLASGOW",
            "G72 0UP"
            ]
        self.assertEqual(self.address.as_list(), address, "Incorrect Mainfile list format")

    def test_string(self):
        """Test conversion to a string"""
        address = (
            "SOUTH LANARKSHIRE COUNCIL, "
            "HEAD START, "
            "UNIT 1, "
            "BLOCK 3, "
            "THIRD ROAD, "
            "BLANTYRE INDUSTRIAL ESTATE, "
            "BLANTYRE, "
            "GLASGOW. "
            "G72 0UP"
            )
        self.assertEqual(self.address.as_str(), address, "Incorrect Mainfile string format")

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = (
            "SOUTH LANARKSHIRE COUNCIL",
            "HEAD START",
            "UNIT 1",
            "BLOCK 3",
            "THIRD ROAD",
            "BLANTYRE INDUSTRIAL ESTATE",
            "BLANTYRE",
            "GLASGOW",
            "G72 0UP"
            )
        self.assertEqual(self.address.as_tuple(), address, "Incorrect Mainfile tuple format")

    def test_dict(self):
        """Test conversion to a dict"""
        address = {
            'line_1': "SOUTH LANARKSHIRE COUNCIL",
            'line_2': "HEAD START",
            'line_3': "UNIT 1",
            'line_4': "BLOCK 3",
            'line_5': "THIRD ROAD",
            'line_6': "BLANTYRE INDUSTRIAL ESTATE",
            'line_7': "BLANTYRE",
            'post_town': "GLASGOW",
            'postcode': "G72 0UP"
            }
        self.assertEqual(self.address.as_dict(), address, "Incorrect Mainfile dict format")

    def test_premises(self):
        """Test premises"""
        premises = {
            'premises_type': 'BLOCK',
            'premises_number': 3,
            'sub_premises_type': 'UNIT',
            'sub_premises_number': 1
            }
        self.assertEqual(self.address.premises(), premises, "Incorrect Mainfile premises")

if __name__ == '__main__':
    unittest.main()
