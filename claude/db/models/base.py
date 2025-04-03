import inspect
import json
import logging
import sqlite3
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple, Type, TypeVar, Union, cast
from bot.db.connection import Database, QueryError, TransactionError, get_db
logger = logging.getLogger(__name__)
T = TypeVar('T', bound='BaseModel')


class ModelError(Exception):
    pass


class ValidationError(ModelError):
    pass


class NotFoundError(ModelError):
    pass


class DuplicateError(ModelError):
    pass


class RelationshipError(ModelError):
    pass


class Field:
    def __init__(
        self,
        field_type: Type,
        primary_key: bool = False,
        unique: bool = False,
        nullable: bool = True,
        default: Any = None,
        foreign_key: Optional[str] = None,
        validators: Optional[List[callable]] = None
    ):
        self.field_type = field_type
        self.primary_key = primary_key
        self.unique = unique
        self.nullable = nullable
        self.default = default
        self.foreign_key = foreign_key
        self.validators = validators or []

    def validate(self, value: Any) -> None:
        if value is None:
            if not self.nullable:
                raise ValidationError(f"Field cannot be NULL")
            return
        if not isinstance(value, self.field_type) and value is not None:
            if self.field_type is bool and isinstance(value, int):
                pass
            else:
                raise ValidationError(
                    f"Expected type {self.field_type.__name__}, got {type(value).__name__}")
        for validator in self.validators:
            try:
                if not validator(value):
                    raise ValidationError(
                        f"Validation failed with validator {validator.__name__}")
            except Exception as e:
                if isinstance(e, ValidationError):
                    raise
                raise ValidationError(str(e)) from e


class Relationship:
    def __init__(
        self,
        related_model: str,
        relation_type: str,
        foreign_key: str,
        back_populates: Optional[str] = None
    ):
        self.related_model = related_model
        self.relation_type = relation_type
        self.foreign_key = foreign_key
        self.back_populates = back_populates


class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        if name == 'BaseModel':
            return super().__new__(mcs, name, bases, attrs)
        fields = {}
        relationships = {}
        table_name = attrs.get('__tablename__')
        if table_name is None:
            import re
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            table_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
            attrs['__tablename__'] = table_name
        for attr_name, attr_value in list(attrs.items()):
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value
                del attrs[attr_name]
            elif isinstance(attr_value, Relationship):
                relationships[attr_name] = attr_value
                del attrs[attr_name]
        attrs['__fields__'] = fields
        attrs['__relationships__'] = relationships
        return super().__new__(mcs, name, bases, attrs)


class BaseModel(metaclass=ModelMeta):
    __tablename__: ClassVar[str] = ''
    __fields__: ClassVar[Dict[str, Field]] = {}
    __relationships__: ClassVar[Dict[str, Relationship]] = {}
    id: Optional[int] = None
    _db: Optional[Database] = None
    _values: Dict[str, Any] = {}
    _loaded_relationships: Dict[str, Any] = {}
    _is_new: bool = True
    _is_deleted: bool = False

    def __init__(self, **kwargs):
        self._values = {}
        self._loaded_relationships = {}
        self._is_new = True
        self._is_deleted = False
        for field_name, value in kwargs.items():
            if field_name in self.__fields__:
                self._values[field_name] = value
            elif field_name == 'id':
                self.id = value
                self._is_new = False
            else:
                pass
        for field_name, field in self.__fields__.items():
            if field_name not in self._values and field.default is not None:
                if callable(field.default):
                    self._values[field_name] = field.default()
                else:
                    self._values[field_name] = field.default

    def __getattr__(self, name: str) -> Any:
        if name in self._values:
            return self._values[name]
        elif name in self.__fields__:
            return None
        elif name in self.__relationships__:
            if name not in self._loaded_relationships:
                self._load_relationship(name)
            return self._loaded_relationships[name]
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            super().__setattr__(name, value)
        elif name == 'id':
            super().__setattr__(name, value)
            if value is not None:
                self._is_new = False
        elif name in self.__fields__:
            field = self.__fields__[name]
            field.validate(value)
            self._values[name] = value
        elif name in self.__relationships__:
            self._loaded_relationships[name] = value
        else:
            super().__setattr__(name, value)

    def get_db(self) -> Database:
        if self._db is None:
            self._db = get_db()
        return self._db

    def to_dict(self) -> Dict[str, Any]:
        result = {'id': self.id}
        result.update(self._values)
        return result

    def from_dict(self, data: Dict[str, Any]) -> 'BaseModel':
        for field_name, value in data.items():
            if field_name == 'id':
                self.id = value
                self._is_new = False
            elif field_name in self.__fields__:
                field = self.__fields__[field_name]
                field.validate(value)
                self._values[field_name] = value

        return self

    def from_row(self, row: sqlite3.Row) -> 'BaseModel':
        if row is None:
            raise NotFoundError("Record not found")
        data = dict(row)
        return self.from_dict(data)

    def validate(self) -> None:
        for field_name, field in self.__fields__.items():
            value = self._values.get(field_name)
            field.validate(value)

    def save(self) -> 'BaseModel':
        self.validate()
        db = self.get_db()
        try:
            if self._is_new:
                data = {k: v for k, v in self._values.items() if v is not None}
                self.id = db.insert(self.__tablename__, data)
                self._is_new = False
                logger.debug(
                    f"Created {self.__class__.__name__} with ID {self.id}")
            else:
                data = {k: v for k, v in self._values.items() if v is not None}
                db.update(self.__tablename__, data, "id = ?", (self.id,))
                logger.debug(
                    f"Updated {self.__class__.__name__} with ID {self.id}")
            return self
        except QueryError as e:
            if "UNIQUE constraint failed" in str(e):
                raise DuplicateError(
                    f"Record already exists with these unique fields") from e
            raise

    def delete(self) -> None:
        if self.id is None:
            raise NotFoundError("Cannot delete a record without an ID")
        if self._is_deleted:
            logger.warning(
                f"{self.__class__.__name__} with ID {self.id} already deleted")
            return
        db = self.get_db()
        db.delete(self.__tablename__, "id = ?", (self.id,))
        self._is_deleted = True
        logger.debug(f"Deleted {self.__class__.__name__} with ID {self.id}")

    def refresh(self) -> 'BaseModel':
        if self.id is None:
            raise NotFoundError("Cannot refresh a record without an ID")
        if self._is_deleted:
            raise NotFoundError(
                f"{self.__class__.__name__} with ID {self.id} has been deleted")
        db = self.get_db()
        query = f"SELECT * FROM {self.__tablename__} WHERE id = ?"
        row = db.fetchone(query, (self.id,))
        if row is None:
            raise NotFoundError(
                f"{self.__class__.__name__} with ID {self.id} not found")
        self.from_row(row)
        self._loaded_relationships.clear()
        return self

    def _load_relationship(self, relationship_name: str) -> None:
        if self.id is None:
            self._loaded_relationships[relationship_name] = None
            return
        relationship = self.__relationships__[relationship_name]
        related_model_name = relationship.related_model
        relation_type = relationship.relation_type
        foreign_key = relationship.foreign_key
        try:
            module_parts = self.__module__.split('.')
            module_paths = [
                '.'.join(module_parts[:-1]) + '.' + related_model_name.lower(),
                self.__module__,
                'bot.db.models.' + related_model_name.lower()
            ]
            related_model_class = None
            for module_path in module_paths:
                try:
                    module = __import__(module_path, fromlist=[
                                        related_model_name])
                    if hasattr(module, related_model_name):
                        related_model_class = getattr(
                            module, related_model_name)
                        break
                except ImportError:
                    continue
            if related_model_class is None:
                raise RelationshipError(
                    f"Could not find related model class '{related_model_name}'")
            if relation_type == 'many_to_one':
                foreign_id = self._values.get(foreign_key)
                if foreign_id is None:
                    self._loaded_relationships[relationship_name] = None
                else:
                    related_instance = related_model_class.get_by_id(
                        foreign_id)
                    self._loaded_relationships[relationship_name] = related_instance
            elif relation_type == 'one_to_many':
                related_instances = related_model_class.find_by(
                    foreign_key, self.id)
                self._loaded_relationships[relationship_name] = related_instances
            elif relation_type == 'many_to_many':
                raise NotImplementedError(
                    "Many-to-many relationships are not implemented yet")
            else:
                raise RelationshipError(
                    f"Unknown relationship type: {relation_type}")
        except Exception as e:
            if isinstance(e, (RelationshipError, NotImplementedError)):
                raise
            raise RelationshipError(
                f"Error loading relationship '{relationship_name}': {str(e)}") from e

    @classmethod
    def get_by_id(cls: Type[T], id: int) -> T:
        db = get_db()
        query = f"SELECT * FROM {cls.__tablename__} WHERE id = ?"
        row = db.fetchone(query, (id,))
        if row is None:
            raise NotFoundError(f"{cls.__name__} with ID {id} not found")
        instance = cls()
        instance.from_row(row)
        instance._is_new = False
        return instance

    @classmethod
    def get_by(cls: Type[T], field: str, value: Any) -> T:
        db = get_db()
        query = f"SELECT * FROM {cls.__tablename__} WHERE {field} = ?"
        row = db.fetchone(query, (value,))
        if row is None:
            raise NotFoundError(
                f"{cls.__name__} with {field}={value} not found")
        instance = cls()
        instance.from_row(row)
        instance._is_new = False
        return instance

    @classmethod
    def find_by(cls: Type[T], field: str, value: Any) -> List[T]:
        db = get_db()
        query = f"SELECT * FROM {cls.__tablename__} WHERE {field} = ?"
        rows = db.fetchall(query, (value,))
        instances = []
        for row in rows:
            instance = cls()
            instance.from_row(row)
            instance._is_new = False
            instances.append(instance)
        return instances

    @classmethod
    def find_all(cls: Type[T]) -> List[T]:
        db = get_db()
        query = f"SELECT * FROM {cls.__tablename__}"
        rows = db.fetchall(query)
        instances = []
        for row in rows:
            instance = cls()
            instance.from_row(row)
            instance._is_new = False
            instances.append(instance)
        return instances

    @classmethod
    def count(cls) -> int:
        db = get_db()
        query = f"SELECT COUNT(*) as count FROM {cls.__tablename__}"
        row = db.fetchone(query)
        if row is None:
            return 0
        return row['count']

    @classmethod
    def exists(cls, id: int) -> bool:
        db = get_db()
        query = f"SELECT 1 FROM {cls.__tablename__} WHERE id = ?"
        row = db.fetchone(query, (id,))
        return row is not None

    @classmethod
    def exists_by(cls, field: str, value: Any) -> bool:
        db = get_db()
        query = f"SELECT 1 FROM {cls.__tablename__} WHERE {field} = ?"
        row = db.fetchone(query, (value,))
        return row is not None

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        instance = cls(**kwargs)
        instance.save()
        return instance

    @classmethod
    def bulk_create(cls: Type[T], records: List[Dict[str, Any]]) -> List[T]:
        db = get_db()
        instances = []
        try:
            with db.transaction():
                for record_data in records:
                    instance = cls(**record_data)
                    instance.save()
                    instances.append(instance)
        except Exception as e:
            logger.error(f"Error in bulk_create: {str(e)}", exc_info=True)
            raise
        return instances

    @classmethod
    def delete_by_id(cls, id: int) -> bool:
        db = get_db()
        result = db.delete(cls.__tablename__, "id = ?", (id,))
        return result > 0

    @classmethod
    def delete_by(cls, field: str, value: Any) -> int:
        db = get_db()
        result = db.delete(cls.__tablename__, f"{field} = ?", (value,))
        return result

    @classmethod
    def query(cls: Type[T], sql: str, params: Optional[Tuple] = None) -> List[T]:
        db = get_db()
        rows = db.fetchall(sql, params)
        instances = []
        for row in rows:
            instance = cls()
            try:
                instance.from_row(row)
                instance._is_new = False
                instances.append(instance)
            except Exception as e:
                logger.warning(
                    f"Error creating instance from query result: {str(e)}", exc_info=True)
                continue
        return instances
