import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from bot.db.models.base import BaseModel, Field, Relationship, ValidationError


def validate_item_type(item_type: str) -> bool:
    return item_type in ['weapon', 'armour', 'toy', 'card', 'mod']


def validate_quantity(quantity: int) -> bool:
    return quantity >= 0


class UserInventoryItem(BaseModel):
    __tablename__ = 'user_inventory_items'
    
    user_id = Field(str, nullable=False)
    item_name = Field(str, nullable=False)
    item_type = Field(str, nullable=False, validators=[validate_item_type])
    quantity = Field(int, nullable=False, default=1, validators=[validate_quantity])
    acquired_date = Field(str, nullable=False, 
                          default=lambda: datetime.now().isoformat())
    
    user = Relationship(
        related_model='User', 
        relation_type='many_to_one', 
        foreign_key='user_id',
        back_populates='inventory_items'
    )

    def add_quantity(self, amount: int = 1) -> int:
        if amount < 0:
            raise ValidationError("Quantity must be non-negative")
        self.quantity += amount
        self.save()
        return self.quantity

    def remove_quantity(self, amount: int = 1) -> int:
        if amount < 0:
            raise ValidationError("Quantity must be non-negative")
        if self.quantity < amount:
            raise ValidationError("Not enough items to remove")
        self.quantity -= amount
        if self.quantity == 0:
            self.delete()
        else:
            self.save()
        return self.quantity

    @classmethod
    def get_or_create(
        cls, 
        user_id: str, 
        item_name: str, 
        item_type: str
    ) -> 'UserInventoryItem':
        try:
            return cls.get_by_unique_key(user_id, item_name, item_type)
        except:
            return cls(
                user_id=user_id, 
                item_name=item_name, 
                item_type=item_type
            )

    @classmethod
    def get_by_unique_key(
        cls, 
        user_id: str, 
        item_name: str, 
        item_type: str
    ) -> 'UserInventoryItem':
        db = cls.get_db(cls)
        query = f"""
            SELECT * FROM {cls.__tablename__} 
            WHERE user_id = ? AND item_name = ? AND item_type = ?
        """
        row = db.fetchone(query, (user_id, item_name, item_type))
        if row is None:
            raise cls.NotFoundError(f"Item not found for user {user_id}")
        
        instance = cls()
        instance.from_row(row)
        return instance

    @classmethod
    def find_by_user_and_type(
        cls, 
        user_id: str, 
        item_type: str
    ) -> List['UserInventoryItem']:
        db = cls.get_db(cls)
        query = f"""
            SELECT * FROM {cls.__tablename__} 
            WHERE user_id = ? AND item_type = ?
        """
        rows = db.fetchall(query, (user_id, item_type))
        return [
            (lambda instance: instance.from_row(row) or instance)(cls()) 
            for row in rows
        ]