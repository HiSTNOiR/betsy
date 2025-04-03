import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from bot.db.models.base import BaseModel, Field, Relationship, NotFoundError, ValidationError
logger = logging.getLogger(__name__)
T = TypeVar('T', bound='BaseItem')


class BaseItem(BaseModel):
    name = Field(str, nullable=False, unique=True)
    cost = Field(int, nullable=False)
    date_added = Field(str, nullable=False,
                       default=lambda: datetime.now().isoformat())

    def purchase(self, user_id: int) -> bool:
        raise NotImplementedError("Subclasses must implement purchase()")

    @classmethod
    def find_by_name(cls: Type[T], name: str) -> Optional[T]:
        try:
            return cls.get_by('name', name)
        except NotFoundError:
            return None


class Armour(BaseItem):
    __tablename__ = 'armour'
    level = Field(int, nullable=False)

    def purchase(self, user_id: int) -> bool:
        from bot.db.models.user import User
        try:
            user = User.get_by_id(user_id)
            if user.points < self.cost:
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) doesn't have enough points to purchase {self.name}")
                return False
            user.remove_points(self.cost, f"Purchased armour: {self.name}")
            user.set_armour(self.name)
            logger.info(
                f"User {user.twitch_username} ({user.id}) purchased armour: {self.name}")
            return True
        except Exception as e:
            logger.error(f"Error purchasing armour: {str(e)}", exc_info=True)
            return False

    @classmethod
    def get_next_level(cls, current_level: int) -> Optional['Armour']:
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
    __tablename__ = 'weapons'
    level = Field(int, nullable=False)

    def purchase(self, user_id: int) -> bool:
        from bot.db.models.user import User
        try:
            user = User.get_by_id(user_id)
            if user.points < self.cost:
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) doesn't have enough points to purchase {self.name}")
                return False
            user.remove_points(self.cost, f"Purchased weapon: {self.name}")
            user.set_weapon(self.name)
            logger.info(
                f"User {user.twitch_username} ({user.id}) purchased weapon: {self.name}")
            return True
        except Exception as e:
            logger.error(f"Error purchasing weapon: {str(e)}", exc_info=True)
            return False

    @classmethod
    def get_next_level(cls, current_level: int) -> Optional['Weapon']:
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
    __tablename__ = 'armour_mods'
    adjective = Field(str, nullable=False)

    def purchase(self, user_id: int) -> bool:
        from bot.db.models.user import User
        from bot.db.models.inventory import UserArmourMod
        try:
            user = User.get_by_id(user_id)
            if user.points < self.cost:
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) doesn't have enough points to purchase {self.name}")
                return False
            if UserArmourMod.exists_by('user_id', user.id) and UserArmourMod.exists_by('mod_id', self.id):
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) already has armour mod: {self.name}")
                return False
            user.remove_points(self.cost, f"Purchased armour mod: {self.name}")
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
    __tablename__ = 'weapon_mods'
    adjective = Field(str, nullable=False)

    def purchase(self, user_id: int) -> bool:
        from bot.db.models.user import User
        from bot.db.models.inventory import UserWeaponMod
        try:
            user = User.get_by_id(user_id)
            if user.points < self.cost:
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) doesn't have enough points to purchase {self.name}")
                return False
            if UserWeaponMod.exists_by('user_id', user.id) and UserWeaponMod.exists_by('mod_id', self.id):
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) already has weapon mod: {self.name}")
                return False
            user.remove_points(self.cost, f"Purchased weapon mod: {self.name}")
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
    __tablename__ = 'toys'
    command = Field(str, nullable=True)

    def purchase(self, user_id: int) -> bool:
        from bot.db.models.user import User
        from bot.db.models.inventory import UserToy
        try:
            user = User.get_by_id(user_id)
            if user.points < self.cost:
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) doesn't have enough points to purchase {self.name}")
                return False
            if UserToy.exists_by('user_id', user.id) and UserToy.exists_by('toy_id', self.id):
                logger.warning(
                    f"User {user.twitch_username} ({user.id}) already has toy: {self.name}")
                return False
            user.remove_points(self.cost, f"Purchased toy: {self.name}")
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
