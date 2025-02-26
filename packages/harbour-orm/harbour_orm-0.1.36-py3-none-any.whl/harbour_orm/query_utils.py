from collections.abc import Iterable


# query_utils.py
def or_(*conditions):
    columns, params = zip(*conditions)
    or_conditions = []
    for index, col in enumerate(columns):
        column_str = f"{col.table}.{col.field}" if col.table else f"{col.field}"
        if col.operator != "IN UNNEST":
            or_conditions.append(f"{column_str} = @{col.param}")
        else:
            or_conditions.append(process_in_unnest_operator(column_str, params[index]))

    return " OR ".join(or_conditions), {k: v for d in params for k, v in d.items()}


def and_(*conditions):
    columns, params = zip(*conditions)
    and_conditions = []
    for index, col in enumerate(columns):
        column_str = f"{col.table}.{col.field}" if col.table else f"{col.field}"
        if col.operator != "IN UNNEST":
            and_conditions.append(f"{column_str} = @{col.param}")
        else:
            and_conditions.append(process_in_unnest_operator(column_str, params[index]))

    return " AND ".join(and_conditions), {k: v for d in params for k, v in d.items()}


def process_in_unnest_operator(column_str, value_dict):
    # 2 possible cases:
    # 1. WHERE value IN UNNEST(field)
    # 2. WHERE field IN UNNEST([values])
    key, value = tuple(value_dict.items())[0]
    if isinstance(value, Iterable) and not isinstance(value, str):
        return f"{column_str} IN UNNEST(@{key})"
    return f"@{key} IN UNNEST({column_str})"
