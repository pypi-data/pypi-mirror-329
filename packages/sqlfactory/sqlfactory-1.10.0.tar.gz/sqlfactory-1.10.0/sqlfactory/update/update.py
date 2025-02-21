"""UPDATE statement builder."""

from __future__ import annotations

from typing import Any, Optional, Self, TypeAlias

from sqlfactory.condition.base import ConditionBase
from sqlfactory.entities import Column, ColumnArg, Table
from sqlfactory.execute import ConditionalExecutableStatement
from sqlfactory.mixins.limit import Limit, WithLimit
from sqlfactory.mixins.where import WithWhere
from sqlfactory.statement import Statement


class UpdateColumn(Statement):
    """
    Represents one field that should be updated.
    """

    def __init__(self, column: ColumnArg, value: Statement | Any) -> None:
        self._column = column if isinstance(column, Column) else Column(column)
        self._value = value

    def __str__(self) -> str:
        return f"{self._column!s} = {str(self._value) if isinstance(self._value, Statement) else '%s'}"

    def __hash__(self) -> int:
        return hash(self._column)

    def __eq__(self, other: UpdateColumn | Any) -> bool:
        if not isinstance(other, UpdateColumn):
            return False

        return str(self._column) == str(other._column)

    @property
    def args(self) -> list[Any]:
        """
        Return arguments for the update statement.
        """
        if isinstance(self._value, Statement):
            return self._value.args

        return [self._value]


class Update(ConditionalExecutableStatement, WithWhere["Update"], WithLimit["Update"]):
    # pylint: disable=too-many-ancestors  # This is intentional, as this class is a combination of multiple mixins.
    """
    Builds `UPDATE` statement SQL query.

    This is conditional SQL statement, so you can check whether it should be executed (would update any columns)
    by calling bool() on it. Also, if you are using execute() method of the statement, the execution won't be
    performed if bool() returns False.

    Examples:

    >>> from sqlfactory import Update, Eq
    >>> Update("table").set("column1", 1).where(Eq("column2", 2))

    >>> from sqlfactory import Update, Table
    >>> t = Table("table")
    >>> Update(t).set(t.column1, 1).where(t.column2 == 2)
    """

    def __init__(
        self, table: Table | str, *fields: UpdateColumn, where: Optional[ConditionBase] = None, limit: Optional[Limit] = None
    ) -> None:
        """
        :param table: Table to update.
        :param fields: List of UpdateColumn instances containing columns to be updated. This is not very pleasant way
            to create the statement, use set() method instead.
        :param where: WHERE condition
        :param limit: Limit number of updated rows
        """
        super().__init__(where=where, limit=limit)

        self.table = table if isinstance(table, Table) else Table(table)
        """Table that should be updated."""

        self.fields: list[UpdateColumn] = list(fields)
        """Fields that should be updated."""

    def __str__(self) -> str:
        """
        Return the UPDATE statement with %s placeholders for arguments.
        """
        if not self.fields:
            raise AttributeError("At least one column must be updated.")

        query = [f"UPDATE {self.table!s}", f"SET {', '.join(map(str, self.fields))}"]

        if self._where:
            query.append("WHERE")
            query.append(str(self._where))

        if self._limit:
            query.append(str(self._limit))

        return " ".join(query)

    @property
    def args(self) -> list[Any]:
        """
        Return all arguments used in the UPDATE statement.
        """
        out = []

        for field in self.fields:
            out.extend(field.args)

        if self._where is not None:
            out.extend(self._where.args)

        if self._limit is not None:
            out.extend(self._limit.args)

        return out

    def __bool__(self) -> bool:
        """
        Return True if there are any fields to be updated and the statement should be executed.
        """
        return bool(self.fields)

    def append(self, field: UpdateColumn) -> Self:
        """
        Append new UpdateField to this UPDATE statement. Can be used when set() method is not sufficient.
        """
        if field in self.fields:
            raise AttributeError(f"Field '{field}' is already in the list of fields to be updated.")

        self.fields.append(field)
        return self

    def set(self, field: ColumnArg, value: Statement | Any) -> Self:
        """
        Syntactical sugar for creating simple SET UpdateFields.
        :param field: Field name (without quotes).
        :param value: Value to set the field to (will be escaped).
        """
        return self.append(UpdateColumn(field, value))

    def SET(self, field: str, value: Any) -> Self:
        # pylint: disable=invalid-name
        """Alias for `Update.set()` for better SQL compatibility (SQL is often written in all caps)."""
        return self.set(field, value)


UPDATE: TypeAlias = Update  # pylint: disable=invalid-name
"""
Alias for Update statement to provide better SQL compatibility, as SQL is often written in all caps.
"""
