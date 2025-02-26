# query_functions.py

from harbour_orm.column import HarbourORMColumn


class QueryFunctions:
    @classmethod
    def count(cls, column: HarbourORMColumn, distinct: bool = False):
        if column:
            column_expression = f"DISTINCT COUNT({column.field})" if distinct else f"COUNT({column.field})"
        else:
            column_expression = "DISTINCT COUNT(*)" if distinct else "COUNT(*)"
        return HarbourORMColumn(None, column_expression)

    @classmethod
    def max(cls, column: HarbourORMColumn):
        if not column:
            raise ValueError("HarbourORMColumn is required for MAX function")
        return HarbourORMColumn(None, f"MAX({column.field})")

    @classmethod
    def min(cls, column: HarbourORMColumn):
        if not column:
            raise ValueError("HarbourORMColumn is required for MIN function")
        return HarbourORMColumn(None, f"MIN({column.field})")

    @classmethod
    def sum(cls, column: HarbourORMColumn):
        if not column:
            raise ValueError("HarbourORMColumn is required for SUM function")
        return HarbourORMColumn(None, f"SUM({column.field})")

    @classmethod
    def avg(cls, column: HarbourORMColumn):
        if not column:
            raise ValueError("HarbourORMColumn is required for AVG function")
        return HarbourORMColumn(None, f"AVG({column.field})")
