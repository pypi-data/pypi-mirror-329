# query_builder.py
from pydantic import BaseModel

from harbour_orm.column import HarbourORMColumn
from harbour_orm.enums import JoinType, OrderDirection, QueryType
from harbour_orm.orm_model import HarbourORMBase
from harbour_orm.query_builder_helpers import _get_exclude_fields
from harbour_orm.query_utils import and_


class QueryBuilder:
    def __init__(self, model):
        self.model = model
        self.table = model.__tablename__
        self.columns = []
        self.joins = []
        self.conditions = []
        self.params = {}
        self.query_type = None
        self.order_cols = []
        self._limit = None
        self._offset = None
        self.return_cols = []
        self._is_column_set = False

    def select(self, *columns):
        self.query_type = QueryType.SELECT
        if columns:
            self.columns = [f"{col.table}.{col.field}" if col.table else f"{col.field}" for col in columns]
            self._is_column_set = True
        return self

    def update(self, *columns):
        new_columns = []
        for column in columns:
            if isinstance(column, BaseModel):
                exclude_fields = _get_exclude_fields(column, is_insert=False)
                filtered_data = column.dict(exclude=exclude_fields)
                new_columns.extend(
                    (
                        HarbourORMColumn(self.model.__tablename__, field) == value
                        for field, value in filtered_data.items()
                    )
                )
            else:
                new_columns.append(column)
        self.query_type = QueryType.UPDATE
        self._set_columns(new_columns)
        return self

    def insert(self, *columns):
        new_columns = []
        for column in columns:
            if isinstance(column, BaseModel):
                exclude_fields = _get_exclude_fields(column, is_insert=True)
                filtered_data = column.dict(exclude=exclude_fields)
                new_columns.extend(
                    (
                        HarbourORMColumn(self.model.__tablename__, field) == value
                        for field, value in filtered_data.items()
                    )
                )
            else:
                new_columns.append(column)
        self.query_type = QueryType.INSERT
        self._set_columns(new_columns)
        return self

    def delete(self):
        self.query_type = QueryType.DELETE
        return self

    def join(self, target_model: HarbourORMBase, *on_conditions, type_of_join: JoinType = JoinType.INNER):
        target_table = target_model.__tablename__
        join_clause = f"{type_of_join.value}"

        # if columns were not set, then select all columns from the current table
        if not self._is_column_set and not self.columns:
            self.columns.append(f"{self.table}.*")

        alias_target_columns = []
        for i, on_condition in enumerate(on_conditions):
            left_condition, right_condition = on_condition

            # if the target condition is the same as the current table, then swap the columns
            source_column, target_column = (
                (right_condition, left_condition)
                if right_condition.table != target_table
                else (left_condition, right_condition)
            )

            target_table_alias = target_column.table
            on_condition_clause = (
                f"{source_column.table}.{source_column.field} = {target_table_alias}.{target_column.field}"
            )
            join_stmt = f"{join_clause} {target_column.table} ON {on_condition_clause}"

            if len(on_conditions) > 1:
                # for multiple join conditions, create aliases for the tables
                target_table_alias = f"{target_column.table}_{i+1}"
                on_condition_clause = (
                    f"{source_column.table}.{source_column.field} = {target_table_alias}.{target_column.field}"
                )
                join_stmt = f"{join_clause} {target_table} AS {target_table_alias} ON {on_condition_clause}"

                if self._is_column_set:
                    # check if columns were set for the target table
                    set_target_columns = [col.split(".") for col in self.columns if col.startswith(target_table)]
                    if set_target_columns:
                        alias_target_columns.extend(
                            [f"{tbl}_{i+1}.{col} AS {col}_{i+1}" for tbl, col in set_target_columns]
                        )
                else:
                    join_table_columns = [
                        f"{target_table_alias}.{col} AS {col}_{i+1}" for col in target_model.__annotations__.keys()
                    ]
                    self.columns.extend(join_table_columns)

            self.joins.append(join_stmt)

        # if columns were not set, then select * columns for joined tables
        if not self._is_column_set and len(on_conditions) == 1:
            self.columns.append(f"{target_table_alias}.*")
        elif alias_target_columns:
            # if columns were set, find index, remove records and then append new aliased target columns
            indexes = [i for i, col in enumerate(self.columns) if col.startswith(target_table)]
            for i in reversed(indexes):
                self.columns.pop(i)
            self.columns.extend(alias_target_columns)

        return self

    def left_join(self, target_model: HarbourORMBase, *on_conditions):
        return self.join(target_model, *on_conditions, type_of_join=JoinType.LEFT)

    def right_join(self, target_model: HarbourORMBase, *on_conditions):
        return self.join(target_model, *on_conditions, type_of_join=JoinType.RIGHT)

    def full_join(self, target_model: HarbourORMBase, *on_conditions):
        return self.join(target_model, *on_conditions, type_of_join=JoinType.FULL)

    def where(self, *conditions):
        for condition in conditions:
            if isinstance(condition, BaseModel):
                exclude_fields = _get_exclude_fields(condition, is_insert=False)
                filtered_data = condition.dict(exclude=exclude_fields)
                pydantic_conditions = (
                    HarbourORMColumn(self.model.__tablename__, field) == value for field, value in filtered_data.items()
                )
                appendable_condition, appendable_param = and_(*pydantic_conditions)
            # most likely it's OR or AND condition
            elif isinstance(condition, tuple) and type(condition[0]) == str:
                appendable_condition, appendable_param = condition
            else:
                appendable_condition, appendable_param = and_(tuple(condition))
            self.conditions.append(appendable_condition)
            self.params.update(appendable_param)
        return self

    def order_by(self, *columns):
        self.order_cols = [f"{col.table}.{col.field} {OrderDirection(col.direction).name}" for col in columns]
        return self

    def limit(self, limit: int = 100):
        self._limit = limit
        return self

    def offset(self, offset: int = 0):
        self._offset = offset
        return self

    def then_return(self, *columns):
        self.return_cols = ["*"]
        if columns:
            self.return_cols = [f"{col.table}.{col.field}" if col.table else f"{col.field}" for col in columns]
        return self

    def build(self, is_total_count: bool = False, **kwargs):
        query = []
        if self.query_type == QueryType.SELECT:
            query.extend(self._build_select(self.columns, is_total_count, **kwargs))
        elif self.query_type == QueryType.UPDATE:
            query.append(self._build_update(self.columns, **kwargs))
        elif self.query_type == QueryType.INSERT:
            query.append(self._build_insert(self.columns, **kwargs))
        elif self.query_type == QueryType.DELETE:
            query.append(self._build_delete(**kwargs))
        if self.conditions:
            query.append(f"WHERE " + " AND ".join(self.conditions))
        if self.order_cols and not is_total_count:
            query.append(f"ORDER BY {', '.join(self.order_cols)}")
        if self._limit and not is_total_count:
            query.append(f"LIMIT {self._limit}")
        if self._offset and not is_total_count:
            query.append(f"OFFSET {self._offset}")
        if self.return_cols:
            query.append(f"THEN RETURN {', '.join(self.return_cols)}")
        return " ".join(query)

    def _build_select(self, columns: list, is_total_count: bool, **kwargs):
        if is_total_count:
            query = [f"SELECT COUNT(*) FROM {self.table}"]
        else:
            query = [f"SELECT {self.table}.* FROM {self.table}"]
            if columns:
                query = [f"SELECT {', '.join(columns)} FROM {self.table}"]
        if self.joins:
            query.extend(self.joins)
        return query

    def _build_update(self, columns: list, **kwargs):
        set_columns = [f"{col.table}.{col.field} = @{col.param}" for col in columns]
        query = f"UPDATE {self.table} SET {', '.join(set_columns)}"
        return query

    def _build_insert(self, columns: list, **kwargs):
        query = f"INSERT INTO {self.table}"
        insert_columns = []
        columns_values = []
        for column in columns:
            insert_columns.append(column.field)
            columns_values.append(f"@{column.param}")
        query += f" ({', '.join(insert_columns)}) VALUES ({', '.join(columns_values)})"
        return query

    def _build_delete(self, **kwargs):
        query = f"DELETE FROM {self.table}"
        return query

    def _set_columns(self, columns: list):
        self.columns = []
        for column, param in columns:
            self.columns.append(column)
            self.params.update(param)

    def __str__(self):
        return self.build()
