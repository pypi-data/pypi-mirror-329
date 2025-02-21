"""
SQLFactory is a Python library for building SQL queries in a programmatic way.

Quick start:

## SELECT ...

Main class of interest: `Select`

Quick example:

```python
from sqlfactory import Select, Eq

query = Select("id", "name", table="products", where=Eq("enabled", True))
```
## INSERT ...

Main class of interest: `Insert`

Quick example:

```python
from sqlfactory import Insert

query = Insert.into("products")("id", "name").values(
    (1, "Product 1"),
    (2, "Product 2"),
)
```

## UPDATE ...

Main class of interest: `Update`

Quick example:

```python
from sqlfactory import Update, Eq

query = Update("products", set={"enabled": False}, where=Eq("id", 1))
```

## DELETE ...

Main class of interest: `Delete`

Quick example:

```python
from sqlfactory import Delete, Eq

query = Delete("products", where=Eq("enabled", False))
```

"""

from sqlfactory import execute, func, mixins  # exported submodules
from sqlfactory.condition import (
    And,
    Between,
    Condition,
    ConditionBase,
    Eq,
    Equals,
    Ge,
    GreaterThan,
    GreaterThanOrEquals,
    Gt,
    In,
    Le,
    LessThan,
    LessThanOrEquals,
    Like,
    Lt,
    Ne,
    NotEquals,
    Or,
)
from sqlfactory.delete import DELETE, Delete
from sqlfactory.entities import Column, Table
from sqlfactory.insert import INSERT, Insert, Values
from sqlfactory.mixins import Direction, Limit, Order
from sqlfactory.select import (
    SELECT,
    Aliased,
    ColumnList,
    CrossJoin,
    InnerJoin,
    Join,
    LeftJoin,
    LeftOuterJoin,
    RightJoin,
    RightOuterJoin,
    Select,
    SelectColumn,
)
from sqlfactory.statement import Raw, Statement
from sqlfactory.update import UPDATE, Update

__all__ = [
    "DELETE",
    "INSERT",
    "SELECT",
    "UPDATE",
    "Aliased",
    "And",
    "Between",
    "Column",
    "ColumnList",
    "Condition",
    "ConditionBase",
    "CrossJoin",
    "Delete",
    "Direction",
    "Eq",
    "Equals",
    "Ge",
    "GreaterThan",
    "GreaterThanOrEquals",
    "Gt",
    "In",
    "InnerJoin",
    "Insert",
    "Join",
    "Le",
    "LeftJoin",
    "LeftOuterJoin",
    "LessThan",
    "LessThanOrEquals",
    "Like",
    "Limit",
    "Lt",
    "Ne",
    "NotEquals",
    "Or",
    "Order",
    "Raw",
    "RightJoin",
    "RightOuterJoin",
    "Select",
    "SelectColumn",
    "Statement",
    "Table",
    "Update",
    "Values",
    "execute",
    "func",
    "mixins",
]
