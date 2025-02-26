# column.py
from google.cloud.spanner_v1 import JsonObject

from harbour_orm.enums import OrderDirection


class HarbourORMColumn:
    _counter = 0

    def __init__(self, table, field):
        self.table = table
        self.field = field
        self.direction = OrderDirection.ASC
        self.operator = None
        self.param = None

    def __del__(self):
        HarbourORMColumn._counter = 0

    def __str__(self) -> str:
        return f"{self.table}.{self.field}"

    def __repr__(self) -> str:
        return f"HarbourORMColumn({self.table}, {self.field})"

    def _generate_param_key(self):
        HarbourORMColumn._counter += 1
        return f"{self.field}_param_{HarbourORMColumn._counter}"

    def __eq__(self, other):
        if isinstance(other, HarbourORMColumn):
            return self, other
        if isinstance(other, dict):
            other = JsonObject(other)
        param_key = self._generate_param_key()
        self.param = param_key
        self.operator = "="
        return self, {param_key: other}

    def __ne__(self, other):
        if isinstance(other, HarbourORMColumn):
            return self, other
        param_key = self._generate_param_key()
        self.param = param_key
        self.operator = "!="
        return self, {param_key: other}

    def __lt__(self, other):
        if isinstance(other, HarbourORMColumn):
            return self, other
        param_key = self._generate_param_key()
        self.param = param_key
        self.operator = "<"
        return self, {param_key: other}

    def __le__(self, other):
        if isinstance(other, HarbourORMColumn):
            return self, other
        param_key = self._generate_param_key()
        self.param = param_key
        self.operator = "<="
        return self, {param_key: other}

    def __gt__(self, other):
        if isinstance(other, HarbourORMColumn):
            return self, other
        param_key = self._generate_param_key()
        self.param = param_key
        self.operator = ">"
        return self, {param_key: other}

    def __ge__(self, other):
        if isinstance(other, HarbourORMColumn):
            return self, other
        param_key = self._generate_param_key()
        self.param = param_key
        self.operator = ">="
        return self, {param_key: other}

    def in_unnest(self, other):
        # 2 possible cases:
        # 1. WHERE value IN UNNEST(field)
        # 2. WHERE field IN UNNEST([values])
        param_key = self._generate_param_key()
        self.param = param_key
        self.operator = "IN UNNEST"
        return self, {param_key: other}

    def asc(self):
        self.direction = OrderDirection.ASC
        return self

    def desc(self):
        self.direction = OrderDirection.DESC
        return self


class ColumnDescriptor:
    def __init__(self, table, field):
        self.table = table
        self.field = field

    def __get__(self, instance, owner):
        return HarbourORMColumn(self.table, self.field)
