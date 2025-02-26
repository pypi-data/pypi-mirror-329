from datetime import date, datetime
from typing import Optional, Type

from google.cloud.spanner_v1 import JsonObject
from google.cloud.spanner_v1 import param_types as spanner_param_types
from google.cloud.spanner_v1.database import Database
from google.cloud.spanner_v1.transaction import Transaction

from harbour_orm.orm_model import HarbourORMBase
from harbour_orm.query_builder import QueryBuilder, QueryType


class HarbourORM:
    def __init__(self, database: Database):
        self._database = database

    @staticmethod
    def query(model: Type["HarbourORMBase"]):
        return QueryBuilder(model)

    def execute(
        self,
        query_builder: QueryBuilder,
        to_dict: bool = False,
        include_total_count: bool = False,
        transaction: Optional[Transaction] = None,
        **kwargs,
    ):
        if query_builder.query_type == QueryType.SELECT:
            return self._read_only(query_builder, to_dict, include_total_count)
        else:
            return self._read_write(query_builder, to_dict, transaction=transaction)

    def _read_only(self, query_builder: QueryBuilder, to_dict: bool, include_total_count: bool, **kwargs):
        sql_query = query_builder.build(**kwargs)
        params, param_types = self.prepare_params(query_builder.params)

        # use multi_use for snapshot if total count is needed
        multi_use = True if include_total_count else False
        with self._database.snapshot(multi_use=multi_use) as snapshot:
            streamed_result = snapshot.execute_sql(sql_query, params=params, param_types=param_types)
            results = streamed_result.to_dict_list() if to_dict else [row for row in list(streamed_result)]

            if include_total_count:

                # skip limit and offset for total count query
                count_sql_query = query_builder.build(is_total_count=True, **kwargs)
                total_count = snapshot.execute_sql(count_sql_query, params=params, param_types=param_types)
                total_count = list(total_count)[0][0]
                return results, total_count
            return results

    def _read_write(
        self, query_builder: QueryBuilder, to_dict: bool, transaction: Optional[Transaction] = None, **kwargs
    ):
        sql_query = query_builder.build(**kwargs)
        params, param_types = self.prepare_params(query_builder.params)

        def execute_in_transaction(txn: Transaction):
            if query_builder.return_cols:
                streamed_result = txn.execute_sql(sql_query, params=params, param_types=param_types)
                results = streamed_result.to_dict_list() if to_dict else [row for row in list(streamed_result)]
            else:
                results = txn.execute_update(sql_query, params=params, param_types=param_types)
            return results

        if transaction is not None:
            # Use provided transaction
            return execute_in_transaction(transaction)
        else:
            # Create new transaction if none provided
            return self._database.run_in_transaction(execute_in_transaction)

    def prepare_params(self, params: dict) -> tuple[dict, dict]:
        """
        Prepares parameters for execution, handling complex types like JSON.

        Args:
            params: The input parameters dictionary

        Returns:
            A tuple of (processed_params, param_types)
        """
        processed_params = {}
        param_types = {}

        for key, value in params.items():
            if isinstance(value, datetime):
                processed_params[key] = value
                param_types[key] = spanner_param_types.TIMESTAMP
            elif isinstance(value, date):
                processed_params[key] = value
                param_types[key] = spanner_param_types.DATE
            elif isinstance(value, dict):
                # Convert dict to JsonObject
                processed_params[key] = JsonObject(value)
                param_types[key] = spanner_param_types.JSON
            elif isinstance(value, list) and value and any(isinstance(item, dict) for item in value):
                # For lists containing dictionaries, keep it as a list but convert each dict to JsonObject
                # This handles ARRAY<JSON> column types in Spanner
                processed_params[key] = [JsonObject(item) if isinstance(item, dict) else item for item in value]
                param_types[key] = spanner_param_types.Array(spanner_param_types.JSON)
            else:
                processed_params[key] = value

        return processed_params, param_types

    # For backward compatibility, maintain the old method but use the new one
    def check_for_datetime(self, params: dict) -> dict:
        """
        Add appropriate param_types for values in the parameters.

        This method is maintained for backward compatibility.

        :param params: The parameters dict
        :return: A dict of parameter types
        """
        _, param_types = self.prepare_params(params)
        return param_types
