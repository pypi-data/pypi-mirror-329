"""VALUES() function for usage in ON DUPLICATE KEY UPDATE statements. MySQL / MariaDB specific."""

from sqlfactory.entities import Column, ColumnArg
from sqlfactory.func.base import Function


class Values(Function):
    # pylint: disable=too-few-public-methods  # Too few public methods, as everything is handled by super class.
    """
    `VALUES(<column>)` for usage in `INSERT INTO ... ON DUPLICATE KEY UPDATE column = VALUES(column)` statements.
    """

    def __init__(self, column: ColumnArg) -> None:
        """
        :param column: Column to be used in `VALUES(<column>)` function.
        """
        if not isinstance(column, Column):
            column = Column(column)

        super().__init__("VALUES", column)
