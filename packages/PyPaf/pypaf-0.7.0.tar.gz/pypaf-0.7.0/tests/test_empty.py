"""Test Empty Address formatting"""

import unittest
import paf

class TestEmpty(unittest.TestCase):
    """Test Address Exception I"""

    def setUp(self):
        """Set up Address instance"""
        self.address = paf.Address({})

    def test_list(self):
        """Test conversion to an list"""
        address = []
        self.assertEqual(self.address.as_list(), address, "Incorrect empty list format")

    def test_string(self):
        """Test conversion to a string"""
        address = ""
        self.assertEqual(self.address.as_str(), address, "Incorrect empty string format")

    def test_tuple(self):
        """Test conversion to a tuple"""
        address = ()
        self.assertEqual(self.address.as_tuple(), address, "Incorrect empty tuple format")

    def test_dict(self):
        """Test conversion to a dict"""
        address = {}
        self.assertEqual(self.address.as_dict(), address, "Incorrect empty dict format")

    def test_premises(self):
        """Test premises"""
        premises = {}
        self.assertEqual(self.address.premises(), premises, "Incorrect empty premises")

if __name__ == '__main__':
    unittest.main()
