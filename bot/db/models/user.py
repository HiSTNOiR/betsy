"""
User model for the database layer.

This module provides the User model for interacting with the users table,
including methods for authentication, points management, and relationships.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from bot.db.models.base import BaseModel, Field, Relationship, NotFoundError, ValidationError

# Set up logger for this module
logger = logging.getLogger(__name__)


# Validator functions
def validate_rank(rank: str) -> bool:
    """Validate user rank."""
    valid_ranks = ['viewer', 'vip', 'subscriber',
                   'moderator', 'broadcaster', 'bot_admin']
    return rank in valid_ranks


def validate_durability(durability: int) -> bool:
    """Validate item durability (0-10)."""
    return 0 <= durability <= 10


class User(BaseModel):
    """
    User model representing a user in the system.

    This model provides methods for user management, authentication,
    and interactions with other models such as items and duels.
    """

    # Table name
    __tablename__ = 'users'

    # Fields
    twitch_user_id = Field(str, unique=True, nullable=True)
    twitch_username = Field(str, nullable=True)
    discord_username = Field(str, nullable=True)
    youtube_username = Field(str, nullable=True)
    rank = Field(str, nullable=False, default='viewer',
                 validators=[validate_rank])
    points = Field(int, nullable=False, default=0)
    points_gifted = Field(int, nullable=False, default=0)
    date_added = Field(str, nullable=False,
                       default=lambda: datetime.now().isoformat())
    last_seen = Field(str, nullable=True)
    weapon = Field(str, nullable=True, default='Rusty Dagger')
    weapon_durability = Field(
        int, nullable=True, default=10, validators=[validate_durability])
    armour = Field(str, nullable=True, default='Tattered Cloth')
    armour_durability = Field(
        int, nullable=True, default=10, validators=[validate_durability])
    duel_wins = Field(int, nullable=False, default=0)
    duel_loses = Field(int, nullable=False, default=0)

    # Relationships
    # These will be dynamically loaded when accessed
    viewing_habits = Relationship(
        related_model='UserViewingHabits',
        relation_type='one_to_many',
        foreign_key='user_id',
        back_populates='user'
    )
    toys = Relationship(
        related_model='UserToy',
        relation_type='one_to_many',
        foreign_key='user_id',
        back_populates='user'
    )
    cards = Relationship(
        related_model='UserCard',
        relation_type='one_to_many',
        foreign_key='user_id',
        back_populates='user'
    )
    weapon_mods = Relationship(
        related_model='UserWeaponMod',
        relation_type='one_to_many',
        foreign_key='user_id',
        back_populates='user'
    )
    armour_mods = Relationship(
        related_model='UserArmourMod',
        relation_type='one_to_many',
        foreign_key='user_id',
        back_populates='user'
    )
    won_duels = Relationship(
        related_model='Duel',
        relation_type='one_to_many',
        foreign_key='winner',
        back_populates='winner_user'
    )
    challenger_duels = Relationship(
        related_model='Duel',
        relation_type='one_to_many',
        foreign_key='challenger',
        back_populates='challenger_user'
    )
    opponent_duels = Relationship(
        related_model='Duel',
        relation_type='one_to_many',
        foreign_key='opponent',
        back_populates='opponent_user'
    )

    def update_last_seen(self) -> None:
        """Update the last seen timestamp for the user."""
        self.last_seen = datetime.now().isoformat()
        self.save()

    def add_points(self, amount: int, reason: str = None) -> int:
        """
        Add points to the user.

        Args:
            amount (int): Amount of points to add.
            reason (str, optional): Reason for adding points.

        Returns:
            int: New points total.

        Raises:
            ValueError: If amount is not a positive integer.
        """
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Amount must be a positive integer")

        self.points += amount
        self.save()

        logger.info(
            f"Added {amount} points to {self.twitch_username} ({self.id}). Reason: {reason}")
        return self.points

    def remove_points(self, amount: int, reason: str = None) -> int:
        """
        Remove points from the user.

        Args:
            amount (int): Amount of points to remove.
            reason (str, optional): Reason for removing points.

        Returns:
            int: New points total.

        Raises:
            ValueError: If amount is not a positive integer.
            ValueError: If user doesn't have enough points.
        """
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Amount must be a positive integer")

        if self.points < amount:
            raise ValueError(
                f"User only has {self.points} points, cannot remove {amount}")

        self.points -= amount
        self.save()

        logger.info(
            f"Removed {amount} points from {self.twitch_username} ({self.id}). Reason: {reason}")
        return self.points

    def gift_points(self, target_user: 'User', amount: int) -> Tuple[int, int]:
        """
        Gift points to another user.

        Args:
            target_user (User): User to receive the points.
            amount (int): Amount of points to gift.

        Returns:
            Tuple[int, int]: Tuple of (sender new balance, receiver new balance).

        Raises:
            ValueError: If amount is not a positive integer.
            ValueError: If user doesn't have enough points.
        """
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Amount must be a positive integer")

        if self.points < amount:
            raise ValueError(
                f"User only has {self.points} points, cannot gift {amount}")

        # Remove points from sender
        self.points -= amount
        self.points_gifted += amount
        self.save()

        # Add points to target
        target_user.points += amount
        target_user.save()

        logger.info(
            f"{self.twitch_username} ({self.id}) gifted {amount} points to {target_user.twitch_username} ({target_user.id})")
        return (self.points, target_user.points)

    def has_enough_points(self, amount: int) -> bool:
        """
        Check if the user has enough points.

        Args:
            amount (int): Amount of points to check.

        Returns:
            bool: True if the user has enough points, False otherwise.
        """
        return self.points >= amount

    def get_total_duel_count(self) -> int:
        """
        Get the total number of duels the user has participated in.

        Returns:
            int: Total duel count.
        """
        return self.duel_wins + self.duel_loses

    def get_win_rate(self) -> float:
        """
        Get the user's duel win rate.

        Returns:
            float: Win rate as a percentage (0-100).
        """
        total_duels = self.get_total_duel_count()
        if total_duels == 0:
            return 0.0
        return (self.duel_wins / total_duels) * 100.0

    def record_duel_win(self) -> None:
        """
        Record a duel win for the user.
        """
        self.duel_wins += 1
        self.save()

    def record_duel_loss(self) -> None:
        """
        Record a duel loss for the user.
        """
        self.duel_loses += 1
        self.save()

    def reduce_weapon_durability(self, amount: int = 1) -> int:
        """
        Reduce the weapon durability.

        Args:
            amount (int): Amount to reduce by.

        Returns:
            int: New durability value.
        """
        if amount < 0:
            raise ValueError("Amount must be non-negative")

        new_durability = max(0, self.weapon_durability - amount)
        self.weapon_durability = new_durability
        self.save()
        return new_durability

    def reduce_armour_durability(self, amount: int = 1) -> int:
        """
        Reduce the armour durability.

        Args:
            amount (int): Amount to reduce by.

        Returns:
            int: New durability value.
        """
        if amount < 0:
            raise ValueError("Amount must be non-negative")

        new_durability = max(0, self.armour_durability - amount)
        self.armour_durability = new_durability
        self.save()
        return new_durability

    def repair_weapon(self, amount: int = 10) -> int:
        """
        Repair the weapon durability.

        Args:
            amount (int): Amount to repair by.

        Returns:
            int: New durability value.
        """
        if amount < 0:
            raise ValueError("Amount must be non-negative")

        new_durability = min(10, self.weapon_durability + amount)
        self.weapon_durability = new_durability
        self.save()
        return new_durability

    def repair_armour(self, amount: int = 10) -> int:
        """
        Repair the armour durability.

        Args:
            amount (int): Amount to repair by.

        Returns:
            int: New durability value.
        """
        if amount < 0:
            raise ValueError("Amount must be non-negative")

        new_durability = min(10, self.armour_durability + amount)
        self.armour_durability = new_durability
        self.save()
        return new_durability

    def set_weapon(self, weapon_name: str) -> None:
        """
        Set the user's weapon.

        Args:
            weapon_name (str): Weapon name.
        """
        self.weapon = weapon_name
        self.weapon_durability = 10  # Reset durability for new weapon
        self.save()

    def set_armour(self, armour_name: str) -> None:
        """
        Set the user's armour.

        Args:
            armour_name (str): Armour name.
        """
        self.armour = armour_name
        self.armour_durability = 10  # Reset durability for new armour
        self.save()

    def promote(self, new_rank: str) -> bool:
        """
        Promote the user to a new rank.

        Args:
            new_rank (str): New rank.

        Returns:
            bool: True if the promotion was successful, False otherwise.

        Raises:
            ValidationError: If the new rank is invalid.
        """
        if not validate_rank(new_rank):
            raise ValidationError(f"Invalid rank: {new_rank}")

        # Define rank hierarchy
        rank_hierarchy = {
            'viewer': 0,
            'subscriber': 1,
            'vip': 2,
            'moderator': 3,
            'broadcaster': 4,
            'bot_admin': 5
        }

        # Check if the new rank is higher than the current rank
        current_rank_level = rank_hierarchy.get(self.rank, 0)
        new_rank_level = rank_hierarchy.get(new_rank, 0)

        if new_rank_level <= current_rank_level:
            return False

        self.rank = new_rank
        self.save()
        logger.info(
            f"User {self.twitch_username} ({self.id}) promoted to {new_rank}")
        return True

    def demote(self, new_rank: str) -> bool:
        """
        Demote the user to a new rank.

        Args:
            new_rank (str): New rank.

        Returns:
            bool: True if the demotion was successful, False otherwise.

        Raises:
            ValidationError: If the new rank is invalid.
        """
        if not validate_rank(new_rank):
            raise ValidationError(f"Invalid rank: {new_rank}")

        # Define rank hierarchy
        rank_hierarchy = {
            'viewer': 0,
            'subscriber': 1,
            'vip': 2,
            'moderator': 3,
            'broadcaster': 4,
            'bot_admin': 5
        }

        # Check if the new rank is lower than the current rank
        current_rank_level = rank_hierarchy.get(self.rank, 0)
        new_rank_level = rank_hierarchy.get(new_rank, 0)

        if new_rank_level >= current_rank_level:
            return False

        self.rank = new_rank
        self.save()
        logger.info(
            f"User {self.twitch_username} ({self.id}) demoted to {new_rank}")
        return True

    @classmethod
    def find_by_twitch_username(cls, twitch_username: str) -> Optional['User']:
        """
        Find a user by Twitch username.

        Args:
            twitch_username (str): Twitch username.

        Returns:
            Optional[User]: User if found, None otherwise.
        """
        try:
            return cls.get_by('twitch_username', twitch_username)
        except NotFoundError:
            return None

    @classmethod
    def find_by_twitch_id(cls, twitch_id: str) -> Optional['User']:
        """
        Find a user by Twitch ID.

        Args:
            twitch_id (str): Twitch ID.

        Returns:
            Optional[User]: User if found, None otherwise.
        """
        try:
            return cls.get_by('twitch_user_id', twitch_id)
        except NotFoundError:
            return None

    @classmethod
    def get_or_create_by_twitch_username(cls, twitch_username: str, twitch_id: str = None) -> 'User':
        """
        Get a user by Twitch username, or create a new one if not found.

        Args:
            twitch_username (str): Twitch username.
            twitch_id (str, optional): Twitch ID.

        Returns:
            User: User instance.
        """
        try:
            user = cls.get_by('twitch_username', twitch_username)

            # Update Twitch ID if it's missing and provided
            if user.twitch_user_id is None and twitch_id:
                user.twitch_user_id = twitch_id
                user.save()

            return user
        except NotFoundError:
            # Create new user
            user = cls(
                twitch_username=twitch_username,
                twitch_user_id=twitch_id,
                date_added=datetime.now().isoformat()
            )
            user.save()
            logger.info(
                f"Created new user {twitch_username} with ID {user.id}")
            return user

    @classmethod
    def get_top_points(cls, limit: int = 10) -> List['User']:
        """
        Get users with the highest points.

        Args:
            limit (int): Maximum number of users to return.

        Returns:
            List[User]: List of users.
        """
        db = cls.get_db(cls)
        query = f"SELECT * FROM {cls.__tablename__} ORDER BY points DESC LIMIT ?"
        rows = db.fetchall(query, (limit,))

        # Create instances from rows
        instances = []
        for row in rows:
            instance = cls()
            instance.from_row(row)
            instance._is_new = False
            instances.append(instance)

        return instances

    @classmethod
    def get_top_gifters(cls, limit: int = 10) -> List['User']:
        """
        Get users who have gifted the most points.

        Args:
            limit (int): Maximum number of users to return.

        Returns:
            List[User]: List of users.
        """
        db = cls.get_db(cls)
        query = f"SELECT * FROM {cls.__tablename__} ORDER BY points_gifted DESC LIMIT ?"
        rows = db.fetchall(query, (limit,))

        # Create instances from rows
        instances = []
        for row in rows:
            instance = cls()
            instance.from_row(row)
            instance._is_new = False
            instances.append(instance)

        return instances
