import uuid
from typing import Any, Mapping, Union
from typing_extensions import Self
from marshmallow import Schema
from flask_sqlalchemy import SQLAlchemy, BaseQuery

db = SQLAlchemy()


class Model:
    query: BaseQuery
    schema: Schema

    def add(self):
        db.session.add(self)
        self.save()

    def update(self, **kwargs):
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])
        self.save()

    def save(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        self.save()

    @classmethod
    def get(cls: Self, obj_id: str) -> Self:
        """Return an instance based on the given primary key identifier, or None if not found.

        E.g.:

        my_user = User.get("unique_id")
        """
        if obj_id is None:
            return None

        return cls.query.get(obj_id)

    @classmethod
    def get_all(cls: Self) -> 'list[Self]':
        """Return a list of all instances of the given Model
        """
        return cls.query.all()

    @classmethod
    def get_by(cls: Self, **kwargs) -> Self:
        """Apply the given filtering criterion using keyword expressions.

        e.g.::

            MyClass.get_by(name='some name')

        :return: The first object that passes the filtering criterion
        """
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_all_by(cls: Self, **kwargs) -> 'list[Self]':
        """Apply the given filtering criterion using keyword expressions.

        e.g.::

            MyClass.get_all_by(name='some name')

        Multiple criteria may be specified as comma separated; the effect
        is that they will be joined together using the :func:`.and_`
        function::

            MyClass.get_all_by(name='some name', id=5)

        :return: List of objects that pass the filtering criterion
        """
        return cls.query.filter_by(**kwargs).all()

    @staticmethod
    def generate_unique_id() -> str:
        return uuid.uuid4().hex

    @classmethod
    def load(cls: Self, data: Mapping[str, Any]) -> Self:
        """Deserialize a data structure to an object defined by this Schema's fields.

        :param data: The data to deserialize.
        :return: Deserialized data
        """
        return cls.schema.load(data)

    @classmethod
    def dump(cls: Self, obj: Self, many: bool = False) -> Union[Self, 'list[Self]']:
        """Serialize an object to native Python data types according to this
        Schema's fields.

        :param obj: The object to serialize.
        :param many: Whether to serialize `obj` as a collection. If `None`, the value
            for `self.many` is used.
        :return: Serialized data
        """
        return cls.schema.dump(obj, many=many)

    @classmethod
    def validate(cls: Self, data, partial=None):
        return cls.schema.validate(data, partial=partial)
