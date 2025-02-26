from typing import TYPE_CHECKING, Set

if TYPE_CHECKING:
    from pydantic import BaseModel


def _get_exclude_fields(db_schema: "BaseModel", where_cols: Set[str] = set(), is_insert: bool = True) -> Set[str]:
    if is_insert:
        include_fields = set(db_schema.dict(exclude_none=True).keys())
    else:
        include_fields = set({**db_schema.dict(exclude_none=True), **db_schema.dict(exclude_unset=True)}.keys())
    exclude_fields = set(db_schema.dict().keys()) - include_fields
    exclude_fields.update(where_cols)
    return exclude_fields
