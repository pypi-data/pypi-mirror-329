"""LIKE statement"""

from typing import Any

from sqlfactory.condition.base import Condition, StatementOrColumn
from sqlfactory.entities import Column
from sqlfactory.statement import Statement


class Like(Condition):
    """
    SQL `LIKE` condition for comparing strings against pattern.

    Examples:

    - Simple
        ```python
        # `column` LIKE %s
        Like("column", "pattern")
        "`column` LIKE %s", ["pattern"]
        ```
    - Negative
        ```python
        # `column` NOT LIKE %s
        Like("column", "pattern", negative=True)
        "`column` NOT LIKE %s", ["pattern"]
        ```
    - Statement
        ```python
        Like("column", Concat("%", Column("other_column"), "%"))
        "`column` LIKE CONCAT(%s, `other_column`, %s)", ["%", "%"]
        ```
    - Statement (negative)
        ```python
        Like("column", Concat("%", Column("other_column"), "%"), negative=True)
        "`column` NOT LIKE CONCAT(%s, `other_column`, %s)", ["%", "%"]
        ```
    - Instead of column, you can also use any other expression
        ```python
        Like(Concat("column", "other_column"), "pattern")
        "CONCAT(`column`, `other_column`) LIKE %s", ["pattern"]
        ```
    """

    def __init__(self, column: StatementOrColumn, value: Any | Statement, negative: bool = False) -> None:
        """
        :param column: Column (or statement) on left side of LIKE operator.
        :param value: Value to match the column (or statement) against.
        :param negative: Whether to use negative matching (NOT LIKE).
        """
        args = []

        if not isinstance(column, Statement):
            column = Column(column)

        if isinstance(column, Statement):
            args.extend(column.args)

        if isinstance(value, Statement):
            args.extend(value.args)
        else:
            args.append(value)

        if isinstance(value, Statement):
            super().__init__(
                f"{column!s}{' NOT' if negative else ''} LIKE {value!s}",
                *args,
            )
        else:
            super().__init__(f"{column!s}{' NOT' if negative else ''} LIKE %s", *args)

    @staticmethod
    def escape(s: str) -> str:
        """
        Escape string for use in LIKE statement
        :param s: String to be escaped
        :return: String with escaped characters - % -> %%, _ -> __, to be safely used as part of pattern in LIKE statement.
        """
        return s.replace("%", "%%").replace("_", "__")
