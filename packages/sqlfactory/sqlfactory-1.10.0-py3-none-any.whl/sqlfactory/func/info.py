"""Information functions (https://mariadb.com/kb/en/information-functions/)."""

from typing import Any

from sqlfactory.entities import Column
from sqlfactory.func.base import Function
from sqlfactory.statement import Raw, Statement


class Benchmark(Function):
    # pylint: disable=too-few-public-methods
    """Executes an expression repeatedly."""

    def __init__(self, count: int, expression: Statement) -> None:
        super().__init__("BENCHMARK", count, expression)


class BinlogGtidPos(Function):
    # pylint: disable=too-few-public-methods
    """Returns a string representation of the corresponding GTID position."""

    def __init__(self) -> None:
        super().__init__("BINLOG_GTID_POS")


class Charset(Function):
    # pylint: disable=too-few-public-methods
    """Returns the character set."""

    def __init__(self) -> None:
        super().__init__("CHARSET")


class Coercibility(Function):
    # pylint: disable=too-few-public-methods
    """Returns the collation coercibility value of the string expression."""

    def __init__(self, expression: str) -> None:
        super().__init__("COERCIBILITY", expression)


class Collation(Function):
    # pylint: disable=too-few-public-methods
    """Collation of the string argument"""

    def __init__(self, expression: str) -> None:
        super().__init__("COLLATION", expression)


class Collate(Raw):
    # pylint: disable=too-few-public-methods
    """String with collation"""

    def __init__(self, expression: str | Statement, collation: str) -> None:
        super().__init__(
            f"{str(expression) if isinstance(expression, Statement) else '%s'} COLLATE {collation}",
            *(
                expression.args
                if isinstance(expression, Statement)
                else [expression]
                if not isinstance(expression, Statement)
                else []
            ),
        )


class ConnectionId(Function):
    # pylint: disable=too-few-public-methods
    """Connection ID"""

    def __init__(self) -> None:
        super().__init__("CONNECTION_ID")


class CurrentRole(Function):
    # pylint: disable=too-few-public-methods
    """Current role name"""

    def __init__(self) -> None:
        super().__init__("CURRENT_ROLE")


class CurrentUser(Function):
    # pylint: disable=too-few-public-methods
    """Username/host that authenticated the current client"""

    def __init__(self) -> None:
        super().__init__("CURRENT_USER")


class Database(Function):
    # pylint: disable=too-few-public-methods
    """Current default database"""

    def __init__(self) -> None:
        super().__init__("DATABASE")


class DecodeHistogram(Function):
    # pylint: disable=too-few-public-methods
    """Returns comma separated numerics corresponding to a probability distribution"""

    def __init__(self, hist_type: Any, histogram: Any) -> None:
        super().__init__("DECODE_HISTOGRAM", hist_type, histogram)


class Default(Function):
    # pylint: disable=too-few-public-methods
    """Returns the default value for a table column"""

    def __init__(self, column: Column) -> None:
        super().__init__("DEFAULT", column)


class FoundRows(Function):
    # pylint: disable=too-few-public-methods
    """Returns the number of (potentially) returned rows if there was no LIMIT involved."""

    def __init__(self) -> None:
        super().__init__("FOUND_ROWS")


class LastInsertId(Function):
    # pylint: disable=too-few-public-methods
    """Returns the value generated for an AUTO_INCREMENT column by the previous INSERT statement."""

    def __init__(self) -> None:
        super().__init__("LAST_INSERT_ID")


class LastValue(Function):
    # pylint: disable=too-few-public-methods
    """Evaluates expression and returns the last."""

    def __init__(self, expr: Statement, *exprs: Statement) -> None:
        super().__init__("LAST_VALUE", expr, *exprs)


class RowNumber(Function):
    # pylint: disable=too-few-public-methods
    """Returns the number of accepted rows so far."""

    def __init__(self) -> None:
        super().__init__("ROW_NUMBER")


class Schema(Function):
    # pylint: disable=too-few-public-methods
    """Current default schema"""

    def __init__(self) -> None:
        super().__init__("SCHEMA")


class SessionUser(Function):
    # pylint: disable=too-few-public-methods
    """Username/host that authenticated the current client"""

    def __init__(self) -> None:
        super().__init__("SESSION_USER")


class SystemUser(Function):
    # pylint: disable=too-few-public-methods
    """Username/host that authenticated the current client"""

    def __init__(self) -> None:
        super().__init__("SYSTEM_USER")


class User(Function):
    # pylint: disable=too-few-public-methods
    """Username/host that authenticated the current client"""

    def __init__(self) -> None:
        super().__init__("USER")


class Version(Function):
    # pylint: disable=too-few-public-methods
    """Database version"""

    def __init__(self) -> None:
        super().__init__("VERSION")
