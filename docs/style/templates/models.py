from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

from core.logging import get_logger
from core.errors import ValidationError, handle_error

logger = get_logger('models')

@dataclass
class BaseModel:
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        try:
            return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        except Exception as e:
            handle_error(ValidationError(f"Error converting {self.__class__.__name__} to dict"))
            return {}

    # EXAMPLE IMPLEMENTATION
    def update(self, **kwargs) -> None:
        try:
            for key, value in kwargs.items():
                if not hasattr(self, key):
                    logger.warning(f"Attempted to update non-existent attribute: {key}")
                    continue
                setattr(self, key, value)
            self.updated_at = datetime.now()
            logger.info(f"{self.__class__.__name__} updated successfully")
        except Exception as e:
            handle_error(ValidationError(f"Error updating {self.__class__.__name__}"))