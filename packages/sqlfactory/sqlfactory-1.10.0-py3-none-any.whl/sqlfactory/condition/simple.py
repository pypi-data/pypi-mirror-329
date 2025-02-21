"""Simple binary comparison conditions."""

from typing import Any, TypeAlias

from sqlfactory.condition.base import Condition, StatementOrColumn
from sqlfactory.statement import Statement


class SimpleCondition(Condition):
    # pylint: disable=too-few-public-methods  # As everything is handled in base classes.
    """
    Simple condition comparing one column with given value, using specified operator.
    """

    def __init__(self, column: StatementOrColumn, operator: str, value: Statement | Any) -> None:
        # pylint: disable=duplicate-code   # It does not make sense to generalize two-row statement used on two places.
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param operator: Operator to use for comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        if not isinstance(column, Statement):
            # pylint: disable=import-outside-toplevel,cyclic-import
            from sqlfactory.entities import Column

            column = Column(column)

        args = []

        if isinstance(column, Statement):
            args.extend(column.args)

        if isinstance(value, Statement):
            args.extend(value.args)

        elif not isinstance(value, Statement):
            args.append(value)

        if isinstance(value, Statement):
            super().__init__(f"{column!s} {operator} {value!s}", *args)
        else:
            super().__init__(f"{column!s} {operator} %s", *args)


class Equals(SimpleCondition):
    # pylint: disable=too-few-public-methods  # As everything is handled in base classes.
    """
    Equality condition (`==`). You can also use shorthand alias `Eq`.

    Note that first argument to `Equals` (or `Eq`) is expected to be column, while second argument is value. So to compare
    two columns, you must use `Column` instances as second argument (`Eq("column1", Column("column2"))` to produce
    ``` `column1` = `column2` ```).

    ```Eq("column1", "column2")``` produces ``` `column1` = %s ``` with arguments ```["column2"]```.

    You can also use column's operator overloading:

    ```python
    c = Column("column")
    c == "value"  # == Eq("column", "value")
    c == None     # == Eq("column", None)
    c == Now()    # == Eq("column", Now())
    ```

    Examples:

    - Simple comparison of column to value
        ```python
        # `column` = <value>
        Eq("column", "value")
        "`column` = %s", ["value"]
        ```
    - Comparison column to None
        ```python
        # `column` IS NULL
        Eq("column", None)
        "`column` IS NULL"
        ```
    - Comparison of generic statement to value
        ```python
        # <statement> = <value>
        Eq(Date(), "2021-01-01")
        "DATE() = %s", ["2021-01-01"]
        ```
    - Comparison of generic statement to None
        ```python
        # <statement> IS NULL
        Eq(Date(), None)
        "DATE() IS NULL"
        ```
    - Comparison of statement to statement
        ```python
        # <statement> = <statement>
        Eq(Date(), Now())
        # "DATE() = NOW()"
        ```
    """

    def __init__(self, column: StatementOrColumn, value: Any | None | Statement) -> None:
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        if value is None:
            super().__init__(column, "IS", value)
        else:
            super().__init__(column, "=", value)


class NotEquals(SimpleCondition):
    # pylint: disable=too-few-public-methods  # As everything is handled in base classes.
    """
    Not equality condition (`!=`). You can also use shorthand alis `Ne`.

    Note that first argument to `NotEquals` (or `Ne`) is expected to be column, while second argument is value. So to compare
    two columns, you must use `Column` instances as second argument (`Ne("column1", Column("column2"))` to produce
    ``` `column1` != `column2` ```).

    ```Ne("column1", "column2")``` produces ``` `column1` != %s ``` with arguments ```["column2"]```.

    You can also use column's operator overloading:

    ```python
    c = Column("column")
    c != "value"  # == Ne("column", "value")
    c != None     # == Ne("column", None)
    c != Now()    # == Ne("column", Now())
    ```

    Examples:

    - Column not equals value
        ```python
        # `column` != <value>
        Ne("column", "value")
        "`column` != %s", ["value"]
        ```
    - Statement not equals value
        ```python
        # <statement> != <value>
        Ne(Date(), "2021-01-01")
        "DATE() != %s", ["2021-01-01"]
        ```
    - Column is not None
        ```python
        # `column` IS NOT NULL
        Ne("column", None)
        "`column` IS NOT NULL"
        ```
    - Statement is not None
        ```python
        # <statement> IS NOT NULL
        Ne(Date(), None)
        "DATE() IS NOT NULL"
        ```
    - Statement not equals statement
        ```python
        # <statement> != <statement>
        Ne(Date(), Now())
        "DATE() != NOW()"
        ```
    """

    def __init__(self, column: StatementOrColumn, value: Any | None | Statement) -> None:
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        if value is None:
            super().__init__(column, "IS NOT", value)
        else:
            super().__init__(column, "!=", value)


class GreaterThanOrEquals(SimpleCondition):
    # pylint: disable=too-few-public-methods  # As everything is handled in base classes.
    """
    Greater than or equal condition (`>=`). You can also use shorthand alis `Ge`.

    Note that first argument to `GreaterThanOrEquals` (or `Ge`) is expected to be column, while second argument is value.
    So to compare two columns, you must use `Column` instances as second argument (`Ge("column1", Column("column2"))` to produce
    ``` `column1` >= `column2` ```).

    ```Ge("column1", "column2")``` produces ``` `column1` >= %s ``` with arguments ```["column2"]```.

    You can also use column's operator overloading:

    ```python
    c = Column("column")
    c >= "value"  # == Ge("column", "value")
    c >= None     # == Ge("column", None)
    c >= Now()    # == Ge("column", Now())
    ```

    Examples:

    - Column is greater or equals to value:
        ```python
        # `column` >= <value>
        Ge("column", 10)
        "`column` >= %s", [10]
        ```
    - Statement is greater or equals to value:
        ```python
        # <statement> >= <value>
        Ge(Date(), "2021-01-01")
        "DATE() >= %s", ["2021-01-01"]
        ```
    - Column is greater or equals to other column
        ```python
        # `column1` >= `column2`
        Ge("column1", Column("column2"))
        "`column1` >= `column2`"
        ```
    - Column is greater or equals to statement
        ```python
        # `column` >= <statement>
        Ge("column", Now())
        "`column` >= NOW()"
        ```
    """

    def __init__(self, column: StatementOrColumn, value: Any | Statement) -> None:
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        super().__init__(column, ">=", value)


class GreaterThan(SimpleCondition):
    # pylint: disable=too-few-public-methods  # As everything is handled in base classes.
    """
    Greater than condition (`>`). You can also use shorthand alis `Gt`.

    Note that first argument to `GreaterThan` (or `Ge`) is expected to be column, while second argument is value.
    So to compare two columns, you must use `Column` instances as second argument (`Gt("column1", Column("column2"))` to produce
    ``` `column1` > `column2` ```).

    ```Gt("column1", "column2")``` produces ``` `column1` > %s ``` with arguments ```["column2"]```.

    You can also use column's operator overloading:

    ```python
    c = Column("column")
    c > "value"  # == Gt("column", "value")
    c > None     # == Gt("column", None)
    c > Now()    # == Gt("column", Now())
    ```

    Examples:

    - Column is greater than value:
        ```python
        # `column` > <value>
        Gt("column", 10)
        "`column` > %s, [10]
        ```
    - Statement is greater than value:
        ```python
        # <statement> > <value>
        Gt(Date(), "2021-01-01")
        "DATE() > %s", ["2021-01-01"]
        ```
    - Column is greater than other column
        ```python
        # `column1` > `column2`
        Gt("column1", Column("column2"))
        "`column1` > `column2`"
        ```
    - Column is greater than statement
        ```python
        # `column` > <statement>
        Gt("column", Now())
        "`column` > NOW()"
        ```
    """

    def __init__(self, column: StatementOrColumn, value: Any | Statement) -> None:
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        super().__init__(column, ">", value)


class LessThanOrEquals(SimpleCondition):
    # pylint: disable=too-few-public-methods  # As everything is handled in base classes.
    """
    Less than or equal condition (`<=`). You can also use shorthand alis `Le`.

    Note that first argument to `LessThanOrEquals` (or `Le`) is expected to be column, while second argument is value.
    So to compare two columns, you must use `Column` instances as second argument (`Le("column1", Column("column2"))` to produce
    ``` `column1` <= `column2` ```).

    ```Le("column1", "column2")``` produces ``` `column1` <= %s ``` with arguments ```["column2"]```.

    You can also use column's operator overloading:

    ```python
    c = Column("column")
    c <= "value"  # == Le("column", "value")
    c <= None     # == Le("column", None)
    c <= Now()    # == Le("column", Now())
    ```

    Examples:

    - Column is lower or equal to value:
        ```python
        # `column` <= <value>
        Le("column", 10)
        "`column` <= %s", [10]
        ```
    - Statement is lower or equal to value
        ```python
        <statement> <= <value>
        Le(Date(), "2021-01-01")
        "DATE() <= %s", ["2021-01-01"]
        ```
    - Column is lower or equal to other column
        ```python
        # `column1` <= `column2`
        Le("column1", Column("column2"))
        "`column1` <= `column2`"
        ```
    - Column is lower or equal to statement
        ```python
        # `column` <= <statement>
        Le("column", Now())
        "`column` <= NOW()"
        ```
    """

    def __init__(self, column: StatementOrColumn, value: Any | Statement) -> None:
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        super().__init__(column, "<=", value)


class LessThan(SimpleCondition):
    # pylint: disable=too-few-public-methods  # As everything is handled in base classes.
    """
    Less than condition (`<`). You can also use shorthand alis `Lt`.

    Note that first argument to `LessThan` (or `Lt`) is expected to be column, while second argument is value.
    So to compare two columns, you must use `Column` instances as second argument (`Lt("column1", Column("column2"))` to produce
    ``` `column1` < `column2` ```).

    ```Lt("column1", "column2")``` produces ``` `column1` < %s ``` with arguments ```["column2"]```.

    You can also use column's operator overloading:

    ```python
    c = Column("column")
    c < "value"  # == Lt("column", "value")
    c < None     # == Lt("column", None)
    c < Now()    # == Lt("column", Now())
    ```

    Examples:

    - Column is lower than value:
        ```python
        # `column` < <value>
        Lt("column", 10)
        "`column` < %s", [10]
        ```
    - Statement is lower than value:
        ```python
        # <statement> < <value>
        Lt(Date(), "2021-01-01")
        "DATE() < %s", ["2021-01-01"]
        ```
    - Column is lower than other column
        ```python
        # `column1` < `column2`
        Lt("column1", Column("column2"))
        "`column1` < `column2`"
        ```
    - Column is lower than statement
        ```python
        # `column` < <statement>
        Lt("column", Now())
        "`column` < NOW()"
        ```
    """

    def __init__(self, column: StatementOrColumn, value: Any | Statement) -> None:
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        super().__init__(column, "<", value)


# Convenient aliases for shorter code.
Eq: TypeAlias = Equals
Ge: TypeAlias = GreaterThanOrEquals
Gt: TypeAlias = GreaterThan
Le: TypeAlias = LessThanOrEquals
Lt: TypeAlias = LessThan
Ne: TypeAlias = NotEquals
