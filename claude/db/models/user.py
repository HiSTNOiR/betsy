import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
from bot.db.models.base import BaseModel, Field, Relationship, NotFoundError, ValidationError
logger = logging.getLogger(__name__)


def validate_rank(rank: str) -> bool:
    valid_ranks = ['viewer', 'vip', 'subscriber',
                   'moderator', 'broadcaster', 'bot_admin']
    return rank in valid_ranks


def validate_durability(durability: int) -> bool:
    return 0 <= durability <= 10


class User(BaseModel):
    __tablename__ = 'users'
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
        self.last_seen = datetime.now().isoformat()
        self.save()

    def add_points(self, amount: int, reason: str = None) -> int:
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Amount must be a positive integer")
        self.points += amount
        self.save()
        logger.info(
            f"Added {amount} points to {self.twitch_username} ({self.id}). Reason: {reason}")
        return self.points

    def remove_points(self, amount: int, reason: str = None) -> int:
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
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Amount must be a positive integer")
        if self.points < amount:
            raise ValueError(
                f"User only has {self.points} points, cannot gift {amount}")
        self.points -= amount
        self.points_gifted += amount
        self.save()
        target_user.points += amount
        target_user.save()
        logger.info(
            f"{self.twitch_username} ({self.id}) gifted {amount} points to {target_user.twitch_username} ({target_user.id})")
        return (self.points, target_user.points)

    def has_enough_points(self, amount: int) -> bool:
        return self.points >= amount

    def get_total_duel_count(self) -> int:
        return self.duel_wins + self.duel_loses

    def get_win_rate(self) -> float:
        total_duels = self.get_total_duel_count()
        if total_duels == 0:
            return 0.0
        return (self.duel_wins / total_duels) * 100.0

    def record_duel_win(self) -> None:
        self.duel_wins += 1
        self.save()

    def record_duel_loss(self) -> None:
        self.duel_loses += 1
        self.save()

    def reduce_weapon_durability(self, amount: int = 1) -> int:
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        new_durability = max(0, self.weapon_durability - amount)
        self.weapon_durability = new_durability
        self.save()
        return new_durability

    def reduce_armour_durability(self, amount: int = 1) -> int:
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        new_durability = max(0, self.armour_durability - amount)
        self.armour_durability = new_durability
        self.save()
        return new_durability

    def repair_weapon(self, amount: int = 10) -> int:
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        new_durability = min(10, self.weapon_durability + amount)
        self.weapon_durability = new_durability
        self.save()
        return new_durability

    def repair_armour(self, amount: int = 10) -> int:
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        new_durability = min(10, self.armour_durability + amount)
        self.armour_durability = new_durability
        self.save()
        return new_durability

    def set_weapon(self, weapon_name: str) -> None:
        self.weapon = weapon_name
        self.weapon_durability = 10
        self.save()

    def set_armour(self, armour_name: str) -> None:
        self.armour = armour_name
        self.armour_durability = 10
        self.save()

    def promote(self, new_rank: str) -> bool:
        if not validate_rank(new_rank):
            raise ValidationError(f"Invalid rank: {new_rank}")
        rank_hierarchy = {
            'viewer': 0,
            'subscriber': 1,
            'vip': 2,
            'moderator': 3,
            'broadcaster': 4,
            'bot_admin': 5
        }
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
        if not validate_rank(new_rank):
            raise ValidationError(f"Invalid rank: {new_rank}")
        rank_hierarchy = {
            'viewer': 0,
            'subscriber': 1,
            'vip': 2,
            'moderator': 3,
            'broadcaster': 4,
            'bot_admin': 5
        }
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
        try:
            return cls.get_by('twitch_username', twitch_username)
        except NotFoundError:
            return None

    @classmethod
    def find_by_twitch_id(cls, twitch_id: str) -> Optional['User']:
        try:
            return cls.get_by('twitch_user_id', twitch_id)
        except NotFoundError:
            return None

    @classmethod
    def get_or_create_by_twitch_username(cls, twitch_username: str, twitch_id: str = None) -> 'User':
        try:
            user = cls.get_by('twitch_username', twitch_username)
            if user.twitch_user_id is None and twitch_id:
                user.twitch_user_id = twitch_id
                user.save()
            return user
        except NotFoundError:
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
        db = cls.get_db(cls)
        query = f"SELECT * FROM {cls.__tablename__} ORDER BY points DESC LIMIT ?"
        rows = db.fetchall(query, (limit,))
        instances = []
        for row in rows:
            instance = cls()
            instance.from_row(row)
            instance._is_new = False
            instances.append(instance)
        return instances

    @classmethod
    def get_top_gifters(cls, limit: int = 10) -> List['User']:
        db = cls.get_db(cls)
        query = f"SELECT * FROM {cls.__tablename__} ORDER BY points_gifted DESC LIMIT ?"
        rows = db.fetchall(query, (limit,))
        instances = []
        for row in rows:
            instance = cls()
            instance.from_row(row)
            instance._is_new = False
            instances.append(instance)
        return instances
