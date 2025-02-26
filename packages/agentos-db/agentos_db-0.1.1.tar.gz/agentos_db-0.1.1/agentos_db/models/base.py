import datetime as dt
import enum
import random
import string
from abc import abstractmethod

from sqlalchemy import MetaData, Column, text
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, declared_attr, relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP, TEXT

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "%(table_name)s_%(column_0_name)s_unique",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    metadata = metadata

    @classmethod
    def __declare_last__(cls):
        for mapper in cls.registry.mappers:
            for rel in mapper.relationships:
                if "passive_deletes" not in rel.info:
                    rel.passive_deletes = True
                if "cascade" not in rel.info:
                    # For one-to-many relationships, use delete-orphan
                    if rel.direction.name == "ONETOMANY":
                        rel.cascade = "all, delete-orphan"
                    # For many-to-one or many-to-many, use just 'all'
                    else:
                        rel.cascade = "all"

    def __repr__(self):
        """
        This method is used to represent the model instance in a more
        readable format.
        """
        try:
            identity = inspect(self).identity
        except:
            identity = self.__dict__
        return f"<{self.__class__.__name__} {identity}>"


class HumanIDMixin:
    __prefix__: str
    __id_length__: int = 16

    @classmethod
    def gen_obj_id(cls, prefix: str = None, length: int = 16):
        """Generate a human-readable ID with prefix"""
        if prefix is None:
            prefix = cls.__prefix__

        characters = string.ascii_letters + string.digits
        random_string = "".join(random.choices(characters, k=length))
        return f"{prefix}_{random_string}"

    @classmethod
    def generate_id(cls):
        return cls.gen_obj_id()
