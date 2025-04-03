"""
Item models for the database layer.

This module provides the base item models (Armour, Weapon, Toy, etc.) for 
interacting with the items tables, including methods for item management and relationships.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from bot.db.models.base import BaseModel, Field, Relationship, NotFoundError, ValidationError

# Set up logger for this module
logger = logging.getLogger(__name__)

# Type variables for type hinting
T = TypeVar('T', bound='BaseItem')


class BaseItem(BaseModel):
    """
    Base class for all item models.

    This class provides common functionality for items such as
    weapons, armour, toys, and mods.
    """

    # Fields that all items have
    name = Field(str, nullable=False, unique=True)
    cost = Field(int, nullable=False)
    date_added = Field(str, nullable=False,
                       default=lambda: datetime.now().isoformat())

    def purchase(self, user_id: int) -> bool:
        """
        Purchase the item for a user.

        This method should be overridden by subclasses.

        Args:
            user_id (int): ID of the user making the purchase.

        Returns:
            bool: True if the purchase was successful, False otherwise.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError("Subclasses must implement purchase()")

    @classmethod
    def find_by_name(cls: Type[T], name: str) -> Optional[T]:
        """
        Find an item by name.

        Args:
            name (str): Item name.

        Returns:
            Optional[T]: Item if found, None otherwise.
        """
        try:
            return cls.get_by('name', name)
        except NotFoundError:
            return None


class Armour(BaseItem):
    """
    Armour model representing an armour item in the shop.

    This model provides methods for armour management and purchase functionality.
    """

    # Table name
    __tablename__ = 'armour'

    # Additional fields specific to armour
    level = Field(int, nullable=False)

    def purchase(self, user_id: int) -> bool:
        """
        Purchase the armour for a user.

        Args:
            user_id (int): ID of the user making the purchase.

        Returns:
            bool: True if the purchase was successful, False otherwise.
        """
        # Import User here to avoid circular imports
        from bot.db.models.user import User

        try:
            user = User.get_by_id(user_id)

            # Check if user has enough points
            if user.points < self.cost:
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) doesn't have enough points to purchase {self.name}")
                return False

            # Deduct points
            user.remove_points(self.cost, f"Purchased armour: {self.name}")

            # Equip the armour
            user.set_armour(self.name)

            logger.info(
                f"User {user.twitch_username} ({user.id}) purchased armour: {self.name}")
            return True
        except Exception as e:
            logger.error(f"Error purchasing armour: {str(e)}", exc_info=True)
            return False

    @classmethod
    def get_next_level(cls, current_level: int) -> Optional['Armour']:
        """
        Get the armour for the next level.

        Args:
            current_level (int): Current armour level.

        Returns:
            Optional[Armour]: Next level armour if found, None otherwise.
        """
        try:
            db = cls.get_db(cls)
            query = f"SELECT * FROM {cls.__tablename__} WHERE level > ? ORDER BY level ASC LIMIT 1"
            row = db.fetchone(query, (current_level,))

            if row is None:
                return None

            armour = cls()
            armour.from_row(row)
            armour._is_new = False
            return armour
        except Exception as e:
            logger.error(
                f"Error getting next level armour: {str(e)}", exc_info=True)
            return None


class Weapon(BaseItem):
    """
    Weapon model representing a weapon item in the shop.

    This model provides methods for weapon management and purchase functionality.
    """

    # Table name
    __tablename__ = 'weapons'

    # Additional fields specific to weapons
    level = Field(int, nullable=False)

    def purchase(self, user_id: int) -> bool:
        """
        Purchase the weapon for a user.

        Args:
            user_id (int): ID of the user making the purchase.

        Returns:
            bool: True if the purchase was successful, False otherwise.
        """
        # Import User here to avoid circular imports
        from bot.db.models.user import User

        try:
            user = User.get_by_id(user_id)

            # Check if user has enough points
            if user.points < self.cost:
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) doesn't have enough points to purchase {self.name}")
                return False

            # Deduct points
            user.remove_points(self.cost, f"Purchased weapon: {self.name}")

            # Equip the weapon
            user.set_weapon(self.name)

            logger.info(
                f"User {user.twitch_username} ({user.id}) purchased weapon: {self.name}")
            return True
        except Exception as e:
            logger.error(f"Error purchasing weapon: {str(e)}", exc_info=True)
            return False

    @classmethod
    def get_next_level(cls, current_level: int) -> Optional['Weapon']:
        """
        Get the weapon for the next level.

        Args:
            current_level (int): Current weapon level.

        Returns:
            Optional[Weapon]: Next level weapon if found, None otherwise.
        """
        try:
            db = cls.get_db(cls)
            query = f"SELECT * FROM {cls.__tablename__} WHERE level > ? ORDER BY level ASC LIMIT 1"
            row = db.fetchone(query, (current_level,))

            if row is None:
                return None

            weapon = cls()
            weapon.from_row(row)
            weapon._is_new = False
            return weapon
        except Exception as e:
            logger.error(
                f"Error getting next level weapon: {str(e)}", exc_info=True)
            return None


class ArmourMod(BaseItem):
    """
    ArmourMod model representing an armour modification item in the shop.

    This model provides methods for armour mod management and purchase functionality.
    """

    # Table name
    __tablename__ = 'armour_mods'

    # Additional fields specific to armour mods
    adjective = Field(str, nullable=False)

    def purchase(self, user_id: int) -> bool:
        """
        Purchase the armour mod for a user.

        Args:
            user_id (int): ID of the user making the purchase.

        Returns:
            bool: True if the purchase was successful, False otherwise.
        """
        # Import User here to avoid circular imports
        from bot.db.models.user import User
        from bot.db.models.inventory import UserArmourMod

        try:
            user = User.get_by_id(user_id)

            # Check if user has enough points
            if user.points < self.cost:
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) doesn't have enough points to purchase {self.name}")
                return False

            # Check if user already has this mod
            if UserArmourMod.exists_by('user_id', user.id) and UserArmourMod.exists_by('mod_id', self.id):
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) already has armour mod: {self.name}")
                return False

            # Deduct points
            user.remove_points(self.cost, f"Purchased armour mod: {self.name}")

            # Add mod to user's inventory
            mod = UserArmourMod(
                user_id=user.id,
                mod_id=self.id,
                date_applied=datetime.now().isoformat()
            )
            mod.save()

            logger.info(
                f"User {user.twitch_username} ({user.id}) purchased armour mod: {self.name}")
            return True
        except Exception as e:
            logger.error(
                f"Error purchasing armour mod: {str(e)}", exc_info=True)
            return False


class WeaponMod(BaseItem):
    """
    WeaponMod model representing a weapon modification item in the shop.

    This model provides methods for weapon mod management and purchase functionality.
    """

    # Table name
    __tablename__ = 'weapon_mods'

    # Additional fields specific to weapon mods
    adjective = Field(str, nullable=False)

    def purchase(self, user_id: int) -> bool:
        """
        Purchase the weapon mod for a user.

        Args:
            user_id (int): ID of the user making the purchase.

        Returns:
            bool: True if the purchase was successful, False otherwise.
        """
        # Import User here to avoid circular imports
        from bot.db.models.user import User
        from bot.db.models.inventory import UserWeaponMod

        try:
            user = User.get_by_id(user_id)

            # Check if user has enough points
            if user.points < self.cost:
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) doesn't have enough points to purchase {self.name}")
                return False

            # Check if user already has this mod
            if UserWeaponMod.exists_by('user_id', user.id) and UserWeaponMod.exists_by('mod_id', self.id):
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) already has weapon mod: {self.name}")
                return False

            # Deduct points
            user.remove_points(self.cost, f"Purchased weapon mod: {self.name}")

            # Add mod to user's inventory
            mod = UserWeaponMod(
                user_id=user.id,
                mod_id=self.id,
                date_applied=datetime.now().isoformat()
            )
            mod.save()

            logger.info(
                f"User {user.twitch_username} ({user.id}) purchased weapon mod: {self.name}")
            return True
        except Exception as e:
            logger.error(
                f"Error purchasing weapon mod: {str(e)}", exc_info=True)
            return False


class Toy(BaseItem):
    """
    Toy model representing a toy item in the shop.

    This model provides methods for toy management and purchase functionality.
    """

    # Table name
    __tablename__ = 'toys'

    # Additional fields specific to toys
    command = Field(str, nullable=True)

    def purchase(self, user_id: int) -> bool:
        """
        Purchase the toy for a user.

        Args:
            user_id (int): ID of the user making the purchase.

        Returns:
            bool: True if the purchase was successful, False otherwise.
        """
        # Import User here to avoid circular imports
        from bot.db.models.user import User
        from bot.db.models.inventory import UserToy

        try:
            user = User.get_by_id(user_id)

            # Check if user has enough points
            if user.points < self.cost:
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) doesn't have enough points to purchase {self.name}")
                return False

            # Check if user already has this toy
            if UserToy.exists_by('user_id', user.id) and UserToy.exists_by('toy_id', self.id):
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) already has toy: {self.name}")
                return False

            # Deduct points
            user.remove_points(self.cost, f"Purchased toy: {self.name}")

            # Add toy to user's inventory
            toy = UserToy(
                user_id=user.id,
                toy_id=self.id,
                date_acquired=datetime.now().isoformat()
            )
            toy.save()

            logger.info(
                f"User {user.twitch_username} ({user.id}) purchased toy: {self.name}")
            return True
        except Exception as e:
            logger.error(f"Error purchasing toy: {str(e)}", exc_info=True)
            return False
