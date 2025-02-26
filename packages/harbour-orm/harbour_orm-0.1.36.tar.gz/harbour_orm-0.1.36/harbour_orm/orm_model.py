# orm_model.py
from typing import ClassVar, get_type_hints

from harbour_orm.column import ColumnDescriptor


class HarbourORMBaseMeta(type):
    def __new__(cls, name, bases, dct):
        # Create the class normally
        new_class = super().__new__(cls, name, bases, dct)

        # Get the table name
        tablename = dct.get("__tablename__", name.lower())
        new_class.__tablename__ = tablename

        # Wrap each attribute in the Column class
        for field_name, field_type in get_type_hints(new_class).items():
            if field_name != "__tablename__":
                column = ColumnDescriptor(tablename, field_name)
                setattr(new_class, field_name, column)

        return new_class


class HarbourORMBase(metaclass=HarbourORMBaseMeta):
    __tablename__: ClassVar[str]
