# tests/test_move.py
import unittest
from game.classes.move import Move # Import the class to test

class TestMove(unittest.TestCase):

    def setUp(self):
        """Set up Move instances for testing."""
        self.tackle_data = {
            "name": "Tackle",
            "type": "Normal",
            "category": "Physical",
            "power": 40,
            "accuracy": 100,
            "pp": 35
        }
        self.tackle = Move(**self.tackle_data)

        self.growl_data = {
            "name": "Growl",
            "type": "Normal",
            "category": "Status",
            "power": 0,
            "accuracy": 100,
            "pp": 40
        }
        self.growl = Move(**self.growl_data)

    def test_initialization(self):
        """Test that Move attributes are initialized correctly."""
        # Test Tackle (Physical Move)
        self.assertEqual(self.tackle.name, self.tackle_data["name"])
        self.assertEqual(self.tackle.type, self.tackle_data["type"])
        self.assertEqual(self.tackle.category, self.tackle_data["category"])
        self.assertEqual(self.tackle.power, self.tackle_data["power"])
        self.assertEqual(self.tackle.accuracy, self.tackle_data["accuracy"])
        self.assertEqual(self.tackle.pp, self.tackle_data["pp"])

        # Test Growl (Status Move)
        self.assertEqual(self.growl.name, self.growl_data["name"])
        self.assertEqual(self.growl.type, self.growl_data["type"])
        self.assertEqual(self.growl.category, self.growl_data["category"])
        self.assertEqual(self.growl.power, self.growl_data["power"])
        self.assertEqual(self.growl.accuracy, self.growl_data["accuracy"])
        self.assertEqual(self.growl.pp, self.growl_data["pp"])

    def test_str_representation(self):
        """Test the __str__ method for correct formatting."""
        expected_tackle_str = "Tackle (Normal) Cat:Physical Pow:40 Acc:100 PP:35"
        self.assertEqual(str(self.tackle), expected_tackle_str)

        expected_growl_str = "Growl (Normal) Cat:Status Pow:0 Acc:100 PP:40"
        self.assertEqual(str(self.growl), expected_growl_str)

if __name__ == '__main__':
    unittest.main() 