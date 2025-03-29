# tests/test_pokemon.py
import unittest
import uuid
from unittest.mock import patch # Used to control randomness in stat gain tests
from game.classes.pokemon import Pokemon # Import the class we want to test

class TestPokemon(unittest.TestCase):

    def setUp(self):
        """Set up a Pokémon instance before each test method."""
        self.pokemon_data = {
            "species_name": "Testachu",
            "types": ["Electric"],
            "level": 5,
            "max_hp": 40,
            "attack": 6,
            "defense": 4,
            "speed": 7
        }
        self.pokemon = Pokemon(**self.pokemon_data)
        # Ensure consistent XP threshold for tests
        self.pokemon.XP_PER_LEVEL = 100

    def test_initialization(self):
        """Test that Pokémon attributes are initialized correctly."""
        self.assertEqual(self.pokemon.species_name, self.pokemon_data["species_name"])
        self.assertEqual(self.pokemon.types, self.pokemon_data["types"])
        self.assertEqual(self.pokemon.level, self.pokemon_data["level"])
        self.assertEqual(self.pokemon.max_hp, self.pokemon_data["max_hp"])
        self.assertEqual(self.pokemon.attack, self.pokemon_data["attack"])
        self.assertEqual(self.pokemon.defense, self.pokemon_data["defense"])
        self.assertEqual(self.pokemon.speed, self.pokemon_data["speed"])

        # Check default/derived values
        self.assertEqual(self.pokemon.current_hp, self.pokemon_data["max_hp"]) # Should start at max HP
        self.assertEqual(self.pokemon.xp, 0) # Should start with 0 XP
        self.assertIsInstance(self.pokemon.id, uuid.UUID) # Check if ID is a UUID object
        self.assertIsNone(self.pokemon.nickname) # Nickname should be None initially
        self.assertEqual(self.pokemon.moves, []) # Moves should be an empty list
        self.assertIsNone(self.pokemon.status) # Status should be None initially

    def test_id_uniqueness(self):
        """Test that two different Pokémon have different IDs."""
        pokemon2 = Pokemon(**self.pokemon_data)
        self.assertNotEqual(self.pokemon.id, pokemon2.id)

    def test_is_fainted(self):
        """Test the is_fainted method."""
        self.assertFalse(self.pokemon.is_fainted()) # Should not be fainted initially

        self.pokemon.current_hp = 0
        self.assertTrue(self.pokemon.is_fainted()) # Should be fainted at 0 HP

        self.pokemon.current_hp = -10
        self.assertTrue(self.pokemon.is_fainted()) # Should be fainted below 0 HP

        self.pokemon.current_hp = 1 # Reset to non-fainted state
        self.assertFalse(self.pokemon.is_fainted())

    def test_str_representation(self):
        """Test the __str__ method."""
        expected_str_no_nickname = "Testachu (Lv.5 Type: Electric, HP: 40/40)"
        self.assertEqual(str(self.pokemon), expected_str_no_nickname)

        self.pokemon.nickname = "Testy"
        expected_str_with_nickname = "Testy (Lv.5 Type: Electric, HP: 40/40)"
        self.assertEqual(str(self.pokemon), expected_str_with_nickname)

        self.pokemon.current_hp = 20
        expected_str_low_hp = "Testy (Lv.5 Type: Electric, HP: 20/40)"
        self.assertEqual(str(self.pokemon), expected_str_low_hp)

    # --- New Tests for XP and Leveling --- 

    def test_gain_xp_no_levelup(self):
        """Test gaining XP without leveling up."""
        self.pokemon.gain_xp(50)
        self.assertEqual(self.pokemon.xp, 50)
        self.assertEqual(self.pokemon.level, 5)

    def test_gain_xp_exact_levelup(self):
        """Test gaining exactly enough XP to level up."""
        initial_stats = (self.pokemon.max_hp, self.pokemon.attack, self.pokemon.defense, self.pokemon.speed)
        self.pokemon.gain_xp(100)
        self.assertEqual(self.pokemon.level, 6)
        self.assertEqual(self.pokemon.xp, 0) # XP should reset to 0 after level up
        # Check stats increased (exact value depends on random, check they are greater)
        self.assertGreater(self.pokemon.max_hp, initial_stats[0])
        self.assertGreater(self.pokemon.attack, initial_stats[1])
        self.assertGreater(self.pokemon.defense, initial_stats[2])
        self.assertGreater(self.pokemon.speed, initial_stats[3])

    def test_gain_xp_levelup_with_remainder(self):
        """Test leveling up with leftover XP."""
        self.pokemon.gain_xp(130)
        self.assertEqual(self.pokemon.level, 6)
        self.assertEqual(self.pokemon.xp, 30) # Should have 30 XP remaining

    def test_gain_xp_multiple_levelup(self):
        """Test gaining enough XP for multiple level ups."""
        initial_stats = (self.pokemon.max_hp, self.pokemon.attack, self.pokemon.defense, self.pokemon.speed)
        self.pokemon.gain_xp(250)
        self.assertEqual(self.pokemon.level, 7) # 5 -> 6 -> 7
        self.assertEqual(self.pokemon.xp, 50) # 250 - 100 - 100 = 50 remaining
        # Check stats increased significantly more than one level up
        self.assertGreater(self.pokemon.max_hp, initial_stats[0] + 2) # Expect at least 2 levels worth of HP gain

    def test_gain_xp_fainted(self):
        """Test that fainted Pokémon cannot gain XP."""
        self.pokemon.current_hp = 0
        self.assertTrue(self.pokemon.is_fainted())
        self.pokemon.gain_xp(50)
        self.assertEqual(self.pokemon.xp, 0)
        self.assertEqual(self.pokemon.level, 5)

    def test_gain_xp_max_level(self):
        """Test XP gain at max level (100)."""
        self.pokemon.level = 99
        self.pokemon.xp = 50
        self.pokemon.gain_xp(100) # Gain 100 XP -> 150 total
        self.assertEqual(self.pokemon.level, 100) # Should level up to 100
        self.assertEqual(self.pokemon.xp, 0) # XP should reset/be capped at max level

        # Try gaining more XP at max level
        level_100_stats = (self.pokemon.max_hp, self.pokemon.attack, self.pokemon.defense, self.pokemon.speed)
        self.pokemon.gain_xp(50)
        self.assertEqual(self.pokemon.level, 100) # Level should not increase
        self.assertEqual(self.pokemon.xp, 0) # XP should remain 0
        # Stats should not change after reaching max level
        self.assertEqual(self.pokemon.max_hp, level_100_stats[0])
        self.assertEqual(self.pokemon.attack, level_100_stats[1])
        self.assertEqual(self.pokemon.defense, level_100_stats[2])
        self.assertEqual(self.pokemon.speed, level_100_stats[3])

    def test_gain_zero_negative_xp(self):
        """Test gaining 0 or negative XP does nothing."""
        self.pokemon.gain_xp(0)
        self.assertEqual(self.pokemon.xp, 0)
        self.assertEqual(self.pokemon.level, 5)

        self.pokemon.gain_xp(-50)
        self.assertEqual(self.pokemon.xp, 0)
        self.assertEqual(self.pokemon.level, 5)

    # Use patch to control the random numbers for predictable stat increase tests
    @patch('random.randint')
    def test_stat_increase_on_levelup(self, mock_randint):
        """Test that stats increase on level up with controlled randomness."""
        # Force randint(1, 2) to always return 1 -> hp_increase = 1 + 2 = 3
        # Force randint(0, 1) to always return 1 -> stat_increase = 1 + 1 = 2
        mock_randint.side_effect = [1, 1] # First call for hp, second for others

        initial_hp = self.pokemon.max_hp
        initial_atk = self.pokemon.attack
        initial_def = self.pokemon.defense
        initial_spd = self.pokemon.speed
        initial_current_hp = self.pokemon.current_hp

        self.pokemon.gain_xp(100) # Trigger level up

        self.assertEqual(self.pokemon.level, 6)
        self.assertEqual(self.pokemon.max_hp, initial_hp + 3)
        self.assertEqual(self.pokemon.attack, initial_atk + 2)
        self.assertEqual(self.pokemon.defense, initial_def + 2)
        self.assertEqual(self.pokemon.speed, initial_spd + 2)
        # Check current HP also increased by the max HP gain
        self.assertEqual(self.pokemon.current_hp, initial_current_hp + 3)


if __name__ == '__main__':
    unittest.main() 