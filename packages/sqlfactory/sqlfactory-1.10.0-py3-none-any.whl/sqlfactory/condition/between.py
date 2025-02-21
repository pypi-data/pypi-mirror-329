"""BETWEEN condition generator"""

from typing import Any

from sqlfactory.condition.base import Condition, StatementOrColumn
from sqlfactory.entities import Column
from sqlfactory.statement import Statement


# pylint: disable=too-few-public-methods  # As everything is handled by base classes.
class Between(Condition):
    # pylint: disable=duplicate-code  # It does not make sense to generalize two-row statement used on two places.
    """
    Provides generation for following syntax:

    - ``` `column` BETWEEN <lower_bound> AND <upper_bound>```
    - ``` `column` NOT BETWEEN <lower_bound> AND <upper_bound>```
    - ```<statement> BETWEEN <lower_bound> AND <upper_bound>```
    - ```<statement> NOT BETWEEN <lower_bound> AND <upper_bound>```

    Usage:

    >>> Between('column', 1, 10)
    >>> "`column` BETWEEN 1 AND 10"

    >>> Between('column', 1, 10, negative=True)
    >>> "`column` NOT BETWEEN 1 AND 10"

    >>> Between(Column('c1') + Column('c2'), 1, 10)
    >>> "(`c1` + `c2`) BETWEEN 1 AND 10"

    >>> Between(Column('c1') + Column('c2'), Column('c3') + Column('c4'), Column('c5') + Column('c6'))
    >>> "(`c1` + `c2`) BETWEEN (`c3` + `c4`) AND (`c5` + `c6`)"

    """

    def __init__(
        self, column: StatementOrColumn, lower_bound: Any | Statement, upper_bound: Any | Statement, *, negative: bool = False
    ) -> None:
        """
        :param column: Column to be compared.
        :param lower_bound: Lower inclusive bound of matching value
        :param upper_bound: Upper inclusive bound of matching value
        :param negative: Whether to negate the condition.
        """

        lower_bound_s = "%s"
        upper_bound_s = "%s"

        if not isinstance(column, Statement):
            column = Column(column)

        args = []

        if isinstance(column, Statement):
            args.extend(column.args)

        if isinstance(lower_bound, Statement):
            lower_bound_s = str(lower_bound)
            if isinstance(lower_bound, Statement):
                args.extend(lower_bound.args)
        else:
            args.append(lower_bound)

        if isinstance(upper_bound, Statement):
            upper_bound_s = str(upper_bound)
            if isinstance(upper_bound, Statement):
                args.extend(upper_bound.args)
        else:
            args.append(upper_bound)

        super().__init__(f"{column!s} {'NOT ' if negative else ''}BETWEEN {lower_bound_s} AND {upper_bound_s}", *args)
