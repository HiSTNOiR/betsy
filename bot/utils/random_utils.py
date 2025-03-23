"""
Random utility functions for the Twitch bot.
"""
import random
import string
import logging
from typing import List, Any, Tuple, Dict, Optional, TypeVar, Union, Sequence

# Set up logger
logger = logging.getLogger(__name__)

# Type variable for generic function
T = TypeVar('T')

def random_choice(items: Sequence[T]) -> T:
    """
    Choose a random item from a sequence.
    
    Args:
        items: Sequence of items to choose from
    
    Returns:
        Randomly selected item
    
    Raises:
        ValueError: If items is empty
    """
    if not items:
        raise ValueError("Cannot select from empty sequence")
    
    return random.choice(items)

def random_choices(items: Sequence[T], count: int, weights: Optional[List[float]] = None) -> List[T]:
    """
    Choose multiple random items from a sequence, with replacement.
    
    Args:
        items: Sequence of items to choose from
        count: Number of items to choose
        weights: Optional list of weights for items
    
    Returns:
        List of randomly selected items
    
    Raises:
        ValueError: If items is empty or count is negative
    """
    if not items:
        raise ValueError("Cannot select from empty sequence")
    
    if count < 0:
        raise ValueError("Count cannot be negative")
    
    return random.choices(items, weights=weights, k=count)

def random_sample(items: Sequence[T], count: int) -> List[T]:
    """
    Choose multiple random items from a sequence, without replacement.
    
    Args:
        items: Sequence of items to choose from
        count: Number of items to choose
    
    Returns:
        List of randomly selected items
    
    Raises:
        ValueError: If items is empty, count is negative, or count > len(items)
    """
    if not items:
        raise ValueError("Cannot select from empty sequence")
    
    if count < 0:
        raise ValueError("Count cannot be negative")
    
    if count > len(items):
        raise ValueError(f"Cannot sample {count} items from sequence of length {len(items)}")
    
    return random.sample(list(items), count)

def random_int(min_value: int, max_value: int) -> int:
    """
    Generate a random integer between min_value and max_value (inclusive).
    
    Args:
        min_value: Minimum value
        max_value: Maximum value
    
    Returns:
        Random integer
    
    Raises:
        ValueError: If min_value > max_value
    """
    if min_value > max_value:
        raise ValueError(f"Minimum value ({min_value}) cannot be greater than maximum value ({max_value})")
    
    return random.randint(min_value, max_value)

def random_float(min_value: float, max_value: float) -> float:
    """
    Generate a random float between min_value and max_value.
    
    Args:
        min_value: Minimum value
        max_value: Maximum value
    
    Returns:
        Random float
    
    Raises:
        ValueError: If min_value > max_value
    """
    if min_value > max_value:
        raise ValueError(f"Minimum value ({min_value}) cannot be greater than maximum value ({max_value})")
    
    return random.uniform(min_value, max_value)

def random_string(length: int, chars: str = string.ascii_letters + string.digits) -> str:
    """
    Generate a random string of specified length.
    
    Args:
        length: Length of string to generate
        chars: Character set to use (default: letters and digits)
    
    Returns:
        Random string
    
    Raises:
        ValueError: If length is negative or chars is empty
    """
    if length < 0:
        raise ValueError("Length cannot be negative")
    
    if not chars:
        raise ValueError("Character set cannot be empty")
    
    return ''.join(random.choice(chars) for _ in range(length))

def shuffle_list(items: List[T]) -> List[T]:
    """
    Shuffle a list in-place and return it.
    
    Args:
        items: List to shuffle
    
    Returns:
        Shuffled list
    """
    random.shuffle(items)
    return items

def weighted_choice(items: List[T], weights: List[float]) -> T:
    """
    Choose an item from a list based on weights.
    
    Args:
        items: List of items to choose from
        weights: List of weights for items
    
    Returns:
        Randomly selected item based on weights
    
    Raises:
        ValueError: If items or weights is empty, or lengths don't match
    """
    if not items:
        raise ValueError("Cannot select from empty list")
    
    if not weights:
        raise ValueError("Weights list cannot be empty")
    
    if len(items) != len(weights):
        raise ValueError(f"Items list length ({len(items)}) must match weights list length ({len(weights)})")
    
    return random.choices(items, weights=weights, k=1)[0]

def random_bool(true_prob: float = 0.5) -> bool:
    """
    Generate a random boolean with specified probability of True.
    
    Args:
        true_prob: Probability of True result (0.0 to 1.0)
    
    Returns:
        Random boolean
    
    Raises:
        ValueError: If true_prob is not between 0 and 1
    """
    if not 0 <= true_prob <= 1:
        raise ValueError(f"Probability must be between 0 and 1, got {true_prob}")
    
    return random.random() < true_prob

def random_element_from_dict(d: Dict[T, Any]) -> T:
    """
    Select a random key from a dictionary.
    
    Args:
        d: Dictionary to select from
    
    Returns:
        Randomly selected key
    
    Raises:
        ValueError: If dictionary is empty
    """
    if not d:
        raise ValueError("Cannot select from empty dictionary")
    
    return random.choice(list(d.keys()))

def calculate_random_odds(percent_chance: float) -> bool:
    """
    Determine if an event with a given percent chance succeeds.
    
    Args:
        percent_chance: Percent chance of success (0 to 100)
    
    Returns:
        True if random roll succeeds, False otherwise
    
    Raises:
        ValueError: If percent_chance is not between 0 and 100
    """
    if not 0 <= percent_chance <= 100:
        raise ValueError(f"Percent chance must be between 0 and 100, got {percent_chance}")
    
    return random.random() * 100 < percent_chance

def generate_seed() -> int:
    """
    Generate a random seed for reproducible randomness.
    
    Returns:
        Random seed value
    """
    return random.randint(0, 2**32 - 1)

def set_seed(seed: int) -> None:
    """
    Set the random seed for reproducible randomness.
    
    Args:
        seed: Seed value
    """
    random.seed(seed)
    logger.debug(f"Random seed set to {seed}")