"""Aggregate functions."""

from typing import Literal

from sqlfactory.entities import Column, ColumnArg
from sqlfactory.func.base import Function
from sqlfactory.statement import Raw, Statement


class AggregateFunction(Function):
    # pylint: disable=too-few-public-methods
    """Base class for aggregate functions"""

    def __init__(self, agg: str, column: ColumnArg | Statement):
        super().__init__(agg, Column(column) if isinstance(column, str) else column)


class Avg(AggregateFunction):
    # pylint: disable=too-few-public-methods
    """AVG(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("AVG", column)


class BitAnd(AggregateFunction):
    # pylint: disable=too-few-public-methods
    """BIT_AND(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("BIT_AND", column)


class BitOr(AggregateFunction):
    # pylint: disable=too-few-public-methods
    """BIT_OR(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("BIT_OR", column)


class BitXor(AggregateFunction):
    # pylint: disable=too-few-public-methods
    """BIT_XOR(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("BIT_XOR", column)


class Count(Function):
    # pylint: disable=too-few-public-methods
    """
    - COUNT(<column>)
    - COUNT(DISTINCT <column>)
    """

    def __init__(self, column: ColumnArg | Literal["*"], *, distinct: bool = False):
        if isinstance(column, str) and column == "*":
            column_stmt: Statement = Raw("*")
        elif isinstance(column, str):
            column_stmt = Column(column)
        else:
            column_stmt = column

        if distinct:
            super().__init__(
                "COUNT", Raw(f"DISTINCT {column_stmt!s}", *column_stmt.args if isinstance(column_stmt, Statement) else [])
            )
        else:
            super().__init__("COUNT", column_stmt)


class Max(AggregateFunction):
    # pylint: disable=too-few-public-methods
    """MAX(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("MAX", column)


class Min(AggregateFunction):
    # pylint: disable=too-few-public-methods
    """MIN(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("MIN", column)


class Std(AggregateFunction):
    # pylint: disable=too-few-public-methods
    """STD(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("STD", column)


class Sum(AggregateFunction):
    # pylint: disable=too-few-public-methods
    """SUM(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("SUM", column)
