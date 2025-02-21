"""Miscellaneous functions (https://mariadb.com/kb/en/miscellaneous-functions/)."""

from sqlfactory.func.base import Function
from sqlfactory.statement import Statement


class GetLock(Function):
    # pylint: disable=too-few-public-methods
    """Tries to obtain a lock with a name."""

    def __init__(self, name: str | Statement, timeout: int | Statement) -> None:
        super().__init__("GET_LOCK", name, timeout)


class Inet6Aton(Function):
    # pylint: disable=too-few-public-methods
    """Converts an IPv6 address from its string representation to a binary string."""

    def __init__(self, ip: str | Statement) -> None:
        super().__init__("INET6_ATON", ip)


class Inet6Ntoa(Function):
    # pylint: disable=too-few-public-methods
    """Converts an IPv6 address from its binary string representation to a string."""

    def __init__(self, ip: str | Statement) -> None:
        super().__init__("INET6_NTOA", ip)


class InetAton(Function):
    # pylint: disable=too-few-public-methods
    """Converts an IPv4 address from its string representation to a number."""

    def __init__(self, ip: str | Statement) -> None:
        super().__init__("INET_ATON", ip)


class InetNtoa(Function):
    # pylint: disable=too-few-public-methods
    """Converts an IP number to a string representation."""

    def __init__(self, ip: int | Statement) -> None:
        super().__init__("INET_NTOA", ip)


class IsFreeLock(Function):
    # pylint: disable=too-few-public-methods
    """Checks whether a named lock is free."""

    def __init__(self, name: str | Statement) -> None:
        super().__init__("IS_FREE_LOCK", name)


class IsIpv4(Function):
    # pylint: disable=too-few-public-methods
    """Checks whether a string is an IPv4 address."""

    def __init__(self, ip: str | Statement) -> None:
        super().__init__("IS_IPV4", ip)


class IsIpv4Compat(Function):
    # pylint: disable=too-few-public-methods
    """Checks whether IPv6 address is a valid IPv4-compatible address."""

    def __init__(self, ip: str | Statement) -> None:
        super().__init__("IS_IPV4_COMPAT", ip)


class IsIpv4Mapped(Function):
    # pylint: disable=too-few-public-methods
    """Checks whether IPv6 is an IPv4-mapped address."""

    def __init__(self, ip: str) -> None:
        super().__init__("IS_IPV4_MAPPED", ip)


class IsIpv6(Function):
    # pylint: disable=too-few-public-methods
    """Checks whether a string is an IPv6 address."""

    def __init__(self, ip: str | Statement) -> None:
        super().__init__("IS_IPV6", ip)


class IsUsedLock(Function):
    # pylint: disable=too-few-public-methods
    """Checks whether a named lock is in use."""

    def __init__(self, name: str | Statement) -> None:
        super().__init__("IS_USED_LOCK", name)


class MasterGtidWait(Function):
    # pylint: disable=too-few-public-methods
    """Waits until the slave reaches a specified GTID position."""

    def __init__(self, gtid_set: str | Statement, timeout: int | Statement | None = None) -> None:
        if timeout is not None:
            super().__init__("MASTER_GTID_WAIT", gtid_set, timeout)
        else:
            super().__init__("MASTER_GTID_WAIT", gtid_set)


class MasterPosWait(Function):
    # pylint: disable=too-few-public-methods
    """Waits until the slave reaches a specified binary log position."""

    def __init__(self, log_file: str | Statement, log_pos: int | Statement, timeout: int | Statement | None = None) -> None:
        if timeout is not None:
            super().__init__("MASTER_POS_WAIT", log_file, log_pos, timeout)
        else:
            super().__init__("MASTER_POS_WAIT", log_file, log_pos)


class ReleaseAllLocks(Function):
    # pylint: disable=too-few-public-methods
    """Releases all named locks."""

    def __init__(self) -> None:
        super().__init__("RELEASE_ALL_LOCKS")


class ReleaseLock(Function):
    # pylint: disable=too-few-public-methods
    """Releases a named lock."""

    def __init__(self, name: str | Statement) -> None:
        super().__init__("RELEASE_LOCK", name)


class Sleep(Function):
    # pylint: disable=too-few-public-methods
    """Sleeps for a specified number of seconds."""

    def __init__(self, seconds: int | Statement) -> None:
        super().__init__("SLEEP", seconds)


class SysGuid(Function):
    # pylint: disable=too-few-public-methods
    """Returns a globally unique identifier."""

    def __init__(self) -> None:
        super().__init__("SYS_GUID")


class Uuid(Function):
    # pylint: disable=too-few-public-methods
    """Returns a universally unique identifier."""

    def __init__(self) -> None:
        super().__init__("UUID")


class UuidShort(Function):
    # pylint: disable=too-few-public-methods
    """Returns a short universally unique identifier."""

    def __init__(self) -> None:
        super().__init__("UUID_SHORT")
