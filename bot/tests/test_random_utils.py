"""
Tests for the random utility module.
"""
import unittest
from unittest.mock import patch
import string
import random

from bot.utils.random_utils import (
    random_choice, random_choices, random_sample, random_int,
    random_float, random_string, shuffle_list, weighted_choice,
    random_bool, random_element_from_dict, calculate_random_odds,
    generate_seed, set_seed
)

class TestRandomUtils(unittest.TestCase):
    """Tests for random utility functions."""
    
    def setUp(self):
        """Set up for each test."""
        # Seed for reproducibility
        random.seed(42)
    
    @patch('random.choice')
    def test_random_choice(self, mock_choice):
        """Test random choice from sequence."""
        mock_choice.return_value = 3
        
        # Normal case
        result = random_choice([1, 2, 3, 4, 5])
        mock_choice.assert_called_with([1, 2, 3, 4, 5])
        self.assertEqual(result, 3)
        
        # Empty sequence
        with self.assertRaises(ValueError):
            random_choice([])
    
    @patch('random.choices')
    def test_random_choices(self, mock_choices):
        """Test multiple random choices from sequence."""
        mock_choices.return_value = [2, 3, 5]
        
        # Normal case
        result = random_choices([1, 2, 3, 4, 5], 3)
        mock_choices.assert_called_with([1, 2, 3, 4, 5], weights=None, k=3)
        self.assertEqual(result, [2, 3, 5])
        
        # With weights
        weights = [0.1, 0.2, 0.3, 0.2, 0.2]
        result = random_choices([1, 2, 3, 4, 5], 3, weights=weights)
        mock_choices.assert_called_with([1, 2, 3, 4, 5], weights=weights, k=3)
        self.assertEqual(result, [2, 3, 5])
        
        # Empty sequence
        with self.assertRaises(ValueError):
            random_choices([], 3)
        
        # Negative count
        with self.assertRaises(ValueError):
            random_choices([1, 2, 3], -1)
    
    @patch('random.sample')
    def test_random_sample(self, mock_sample):
        """Test random sampling from sequence."""
        mock_sample.return_value = [2, 5, 3]
        
        # Normal case
        result = random_sample([1, 2, 3, 4, 5], 3)
        mock_sample.assert_called_with([1, 2, 3, 4, 5], 3)
        self.assertEqual(result, [2, 5, 3])
        
        # Empty sequence
        with self.assertRaises(ValueError):
            random_sample([], 3)
        
        # Negative count
        with self.assertRaises(ValueError):
            random_sample([1, 2, 3], -1)
        
        # Count > len(items)
        with self.assertRaises(ValueError):
            random_sample([1, 2, 3], 4)
    
    @patch('random.randint')
    def test_random_int(self, mock_randint):
        """Test random integer generation."""
        mock_randint.return_value = 42
        
        # Normal case
        result = random_int(1, 100)
        mock_randint.assert_called_with(1, 100)
        self.assertEqual(result, 42)
        
        # min_value > max_value
        with self.assertRaises(ValueError):
            random_int(100, 1)
    
    @patch('random.uniform')
    def test_random_float(self, mock_uniform):
        """Test random float generation."""
        mock_uniform.return_value = 42.5
        
        # Normal case
        result = random_float(1.0, 100.0)
        mock_uniform.assert_called_with(1.0, 100.0)
        self.assertEqual(result, 42.5)
        
        # min_value > max_value
        with self.assertRaises(ValueError):
            random_float(100.0, 1.0)
    
    def test_random_string(self):
        """Test random string generation."""
        # Fixed seed for reproducibility
        random.seed(42)
        
        # Length and character set
        length = 10
        chars = string.ascii_lowercase
        
        # Generate random string
        result = random_string(length, chars)
        
        # Check length
        self.assertEqual(len(result), length)
        
        # Check all characters are from the set
        for char in result:
            self.assertIn(char, chars)
        
        # Default character set
        result = random_string(length)
        self.assertEqual(len(result), length)
        
        # Negative length
        with self.assertRaises(ValueError):
            random_string(-1)
        
        # Empty character set
        with self.assertRaises(ValueError):
            random_string(10, "")
    
    @patch('random.shuffle')
    def test_shuffle_list(self, mock_shuffle):
        """Test list shuffling."""
        # Mock shuffle to not actually modify the list
        def side_effect(lst):
            lst[:] = [3, 1, 4, 2, 5]
        mock_shuffle.side_effect = side_effect
        
        # Normal case
        items = [1, 2, 3, 4, 5]
        result = shuffle_list(items)
        mock_shuffle.assert_called_with(items)
        self.assertEqual(result, [3, 1, 4, 2, 5])
        
        # Empty list
        empty = []
        result = shuffle_list(empty)
        mock_shuffle.assert_called_with(empty)
        self.assertEqual(result, [])
    
    @patch('random.choices')
    def test_weighted_choice(self, mock_choices):
        """Test weighted choice."""
        mock_choices.return_value = [3]
        
        # Normal case
        items = [1, 2, 3, 4, 5]
        weights = [0.1, 0.2, 0.4, 0.2, 0.1]
        result = weighted_choice(items, weights)
        mock_choices.assert_called_with(items, weights=weights, k=1)
        self.assertEqual(result, 3)
        
        # Empty list
        with self.assertRaises(ValueError):
            weighted_choice([], [])
        
        # Empty weights
        with self.assertRaises(ValueError):
            weighted_choice([1, 2, 3], [])
        
        # Mismatched lengths
        with self.assertRaises(ValueError):
            weighted_choice([1, 2, 3], [0.5, 0.5])
    
    @patch('random.random')
    def test_random_bool(self, mock_random):
        """Test random boolean generation."""
        # Below threshold
        mock_random.return_value = 0.3
        self.assertTrue(random_bool(0.5))
        
        # Above threshold
        mock_random.return_value = 0.7
        self.assertFalse(random_bool(0.5))
        
        # Custom probability
        mock_random.return_value = 0.2
        self.assertTrue(random_bool(0.3))
        
        # Invalid probability
        with self.assertRaises(ValueError):
            random_bool(1.5)
        with self.assertRaises(ValueError):
            random_bool(-0.5)
    
    @patch('random.choice')
    def test_random_element_from_dict(self, mock_choice):
        """Test random element from dictionary."""
        mock_choice.return_value = 'b'
        
        # Normal case
        d = {'a': 1, 'b': 2, 'c': 3}
        result = random_element_from_dict(d)
        mock_choice.assert_called_with(['a', 'b', 'c'])
        self.assertEqual(result, 'b')
        
        # Empty dict
        with self.assertRaises(ValueError):
            random_element_from_dict({})
    
    @patch('random.random')
    def test_calculate_random_odds(self, mock_random):
        """Test random odds calculation."""
        # Below threshold (success)
        mock_random.return_value = 0.3
        self.assertTrue(calculate_random_odds(50))
        
        # Above threshold (failure)
        mock_random.return_value = 0.6
        self.assertFalse(calculate_random_odds(50))
        
        # 100% chance (always success)
        mock_random.return_value = 0.99
        self.assertTrue(calculate_random_odds(100))
        
        # 0% chance (always failure)
        mock_random.return_value = 0.01
        self.assertFalse(calculate_random_odds(0))
        
        # Invalid percent chance
        with self.assertRaises(ValueError):
            calculate_random_odds(101)
        with self.assertRaises(ValueError):
            calculate_random_odds(-1)
    
    @patch('random.randint')
    def test_generate_seed(self, mock_randint):
        """Test seed generation."""
        mock_randint.return_value = 42
        
        # Generate seed
        seed = generate_seed()
        mock_randint.assert_called_with(0, 2**32 - 1)
        self.assertEqual(seed, 42)
    
    @patch('random.seed')
    def test_set_seed(self, mock_seed):
        """Test setting random seed."""
        # Set seed
        set_seed(42)
        mock_seed.assert_called_with(42)

if __name__ == '__main__':
    unittest.main()