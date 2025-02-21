"""String functions (https://mariadb.com/kb/en/string-functions/)"""

from typing import Any

from sqlfactory.func.base import Function
from sqlfactory.statement import Statement


class Ascii(Function):
    # pylint: disable=too-few-public-methods
    """Numeric ASCII value of leftmost character."""

    def __init__(self, arg: Statement | Any) -> None:
        super().__init__("ASCII", arg)


class Bin(Function):
    # pylint: disable=too-few-public-methods
    """Returns binary value"""

    def __init__(self, num: Statement | Any) -> None:
        super().__init__("BIN", num)


class BitLength(Function):
    # pylint: disable=too-few-public-methods
    """Returns the length of a string in bits"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("BIT_LENGTH", s)


class Char(Function):
    # pylint: disable=too-few-public-methods
    """Returns string based on the integer values for the individual characters."""

    def __init__(self, *n: Statement | int) -> None:
        super().__init__("CHAR", *n)


class CharLength(Function):
    # pylint: disable=too-few-public-methods
    """Length of the string in characters."""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("CHAR_LENGTH", s)


class Chr(Function):
    # pylint: disable=too-few-public-methods
    """Returns string based on integer values of the individual characters."""

    def __init__(self, n: Statement | int) -> None:
        super().__init__("CHR", n)


class Concat(Function):
    # pylint: disable=too-few-public-methods
    """Returns concatenated string"""

    def __init__(self, *s: Statement | Any) -> None:
        super().__init__("CONCAT", *s)


class ConcatWs(Function):
    # pylint: disable=too-few-public-methods
    """Concatenate with separator"""

    def __init__(self, separator: Statement | Any, *s: Statement | Any) -> None:
        super().__init__("CONCAT_WS", separator, *s)


class Hex(Function):
    # pylint: disable=too-few-public-methods
    """Returns a hexadecimal string representation of a decimal or string value."""

    def __init__(self, n: Statement | Any) -> None:
        super().__init__("HEX", n)


class InStr(Function):
    # pylint: disable=too-few-public-methods
    """Returns the position of the first occurrence of substring in string"""

    def __init__(self, s: Statement | Any, substring: Statement | Any) -> None:
        super().__init__("INSTR", s, substring)


class Left(Function):
    # pylint: disable=too-few-public-methods
    """Returns the leftmost number of characters"""

    def __init__(self, s: Statement | Any, n: Statement | int) -> None:
        super().__init__("LEFT", s, n)


class Length(Function):
    # pylint: disable=too-few-public-methods
    """Returns the length of a string"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("LENGTH", s)


class Locate(Function):
    # pylint: disable=too-few-public-methods
    """Returns the position of the first occurrence of substring in string"""

    def __init__(self, substring: Statement | Any, s: Statement | Any) -> None:
        super().__init__("LOCATE", substring, s)


class Lower(Function):
    # pylint: disable=too-few-public-methods
    """Converts a string to lower-case"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("LOWER", s)


class Lpad(Function):
    # pylint: disable=too-few-public-methods
    """Left-pad a string with another string"""

    def __init__(self, s: Statement | Any, n: Statement | int, pad: Statement | Any) -> None:
        super().__init__("LPAD", s, n, pad)


class Ltrim(Function):
    # pylint: disable=too-few-public-methods
    """Removes leading spaces"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("LTRIM", s)


class Mid(Function):
    # pylint: disable=too-few-public-methods
    """Returns a substring"""

    def __init__(self, s: Statement | Any, start: Statement | int, length: Statement | int) -> None:
        super().__init__("MID", s, start, length)


class OctetLength(Function):
    # pylint: disable=too-few-public-methods
    """Returns the length of a string in bytes"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("OCTET_LENGTH", s)


class Ord(Function):
    # pylint: disable=too-few-public-methods
    """Numeric value of leftmost character"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("ORD", s)


class Repeat(Function):
    # pylint: disable=too-few-public-methods
    """Repeat a string the specified number of times"""

    def __init__(self, s: Statement | Any, n: Statement | int) -> None:
        super().__init__("REPEAT", s, n)


class Replace(Function):
    # pylint: disable=too-few-public-methods
    """Replace occurrences of a specified string"""

    def __init__(self, s: Statement | Any, from_: Statement | Any, to: Statement | Any) -> None:
        super().__init__("REPLACE", s, from_, to)


class Reverse(Function):
    # pylint: disable=too-few-public-methods
    """Reverse a string"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("REVERSE", s)


class Right(Function):
    # pylint: disable=too-few-public-methods
    """Returns the rightmost number of characters"""

    def __init__(self, s: Statement | Any, n: Statement | int) -> None:
        super().__init__("RIGHT", s, n)


class RPad(Function):
    # pylint: disable=too-few-public-methods
    """Right-pad a string with another string"""

    def __init__(self, s: Statement | Any, n: Statement | int, pad: Statement | Any) -> None:
        super().__init__("RPAD", s, n, pad)


class RTrim(Function):
    # pylint: disable=too-few-public-methods
    """Removes trailing spaces"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("RTRIM", s)


class SFormat(Function):
    # pylint: disable=too-few-public-methods
    """Format a string"""

    def __init__(self, format_: Statement | Any, *args: Statement | Any) -> None:
        super().__init__("SFORMAT", format_, *args)


class Space(Function):
    # pylint: disable=too-few-public-methods
    """Returns a string of spaces"""

    def __init__(self, n: Statement | int) -> None:
        super().__init__("SPACE", n)


class Substr(Function):
    # pylint: disable=too-few-public-methods
    """Returns a substring"""

    def __init__(self, s: Statement | Any, start: Statement | int, length: Statement | int) -> None:
        super().__init__("SUBSTR", s, start, length)


class Substring(Function):
    # pylint: disable=too-few-public-methods
    """Returns a substring"""

    def __init__(self, s: Statement | Any, start: Statement | int, length: Statement | int) -> None:
        super().__init__("SUBSTRING", s, start, length)


class SubstringIndex(Function):
    # pylint: disable=too-few-public-methods
    """Returns a substring"""

    def __init__(self, s: Statement | Any, delimiter: Statement | Any, count: Statement | int) -> None:
        super().__init__("SUBSTRING_INDEX", s, delimiter, count)


class ToBase64(Function):
    # pylint: disable=too-few-public-methods
    """Converts a string to base64"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("TO_BASE64", s)


class ToChar(Function):
    # pylint: disable=too-few-public-methods
    """Converts a date/time/timestamp type expression to a string"""

    def __init__(self, n: Statement | Any) -> None:
        super().__init__("TO_CHAR", n)


class Trim(Function):
    # pylint: disable=too-few-public-methods
    """Removes leading and trailing spaces"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("TRIM", s)


class Unhex(Function):
    # pylint: disable=too-few-public-methods
    """Converts a hexadecimal pairs of digits to the character represented by the number."""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("UNHEX", s)


class Upper(Function):
    # pylint: disable=too-few-public-methods
    """Converts a string to upper-case"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("UPPER", s)
