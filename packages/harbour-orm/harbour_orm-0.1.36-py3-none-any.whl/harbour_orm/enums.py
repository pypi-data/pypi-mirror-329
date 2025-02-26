from enum import Enum


class QueryType(Enum):
    SELECT = 0
    INSERT = 1
    UPDATE = 2
    DELETE = 3


class OrderDirection(Enum):
    ASC = 0
    DESC = 1


class JoinType(Enum):
    INNER = "JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL JOIN"
    CROSS = "CROSS JOIN"
