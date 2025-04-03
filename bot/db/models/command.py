import json
import logging
from datetime import datetime
from typing import Dict, Optional, List, Any
from bot.db.models.base import BaseModel, Field, ValidationError
from bot.db.models.user import User


def validate_command_action_type(action_type: str) -> bool:
    return action_type in [
        'chat_message', 
        'obs_trigger', 
        'discord_message', 
        'twitch_action', 
        'external_script'
    ]


def validate_action_details(details: str) -> bool:
    try:
        data = json.loads(details)
        return isinstance(data, dict)
    except (json.JSONDecodeError, TypeError):
        return False


class Command(BaseModel):
    __tablename__ = 'commands'

    name = Field(str, unique=True, nullable=False)
    aliases = Field(str, nullable=True)
    description = Field(str, nullable=True)
    action_type = Field(str, nullable=False, validators=[validate_command_action_type])
    action_details = Field(str, nullable=False, validators=[validate_action_details])
    total_uses = Field(int, default=0, nullable=False)
    created_at = Field(str, default=lambda: datetime.now().isoformat(), nullable=False)
    last_used_at = Field(str, nullable=True)
    min_rank = Field(str, default='viewer', nullable=False)

    def increment_uses(self) -> int:
        self.total_uses += 1
        self.last_used_at = datetime.now().isoformat()
        self.save()
        return self.total_uses

    def update_action(self, new_details: Dict[str, Any]) -> None:
        try:
            action_details_str = json.dumps(new_details)
            validate_action_details(action_details_str)
            self.action_details = action_details_str
            self.save()
        except (ValidationError, json.JSONDecodeError) as e:
            raise ValidationError(f"Invalid action details: {str(e)}")

    def is_user_allowed(self, user: User) -> bool:
        rank_hierarchy = {
            'viewer': 0,
            'subscriber': 1,
            'vip': 2,
            'moderator': 3,
            'broadcaster': 4,
            'bot_admin': 5
        }
        return rank_hierarchy.get(user.rank, 0) >= rank_hierarchy.get(self.min_rank, 0)

    @classmethod
    def find_by_name_or_alias(cls, name: str) -> Optional['Command']:
        db = cls.get_db(cls)
        query = f"""
            SELECT * FROM {cls.__tablename__} 
            WHERE name = ? OR aliases LIKE ?
        """
        row = db.fetchone(query, (name, f'%{name}%'))
        if row is None:
            return None
        
        instance = cls()
        instance.from_row(row)
        return instance

    @classmethod
    def get_commands_by_min_rank(cls, min_rank: str) -> List['Command']:
        db = cls.get_db(cls)
        query = f"""
            SELECT * FROM {cls.__tablename__} 
            WHERE min_rank = ?
        """
        rows = db.fetchall(query, (min_rank,))
        return [
            (lambda instance: instance.from_row(row) or instance)(cls()) 
            for row in rows
        ]

    def export_config(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'aliases': self.aliases.split(',') if self.aliases else [],
            'description': self.description,
            'action_type': self.action_type,
            'action_details': json.loads(self.action_details),
            'total_uses': self.total_uses,
            'min_rank': self.min_rank
        }