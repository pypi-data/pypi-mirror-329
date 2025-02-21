"""Encryption functions (https://mariadb.com/kb/en/encryption-hashing-and-compression-functions/)"""

from typing import Any, Literal, Optional

from sqlfactory.func.base import Function
from sqlfactory.statement import Statement


class AesDecrypt(Function):
    # pylint: disable=too-few-public-methods
    """
    Decrypts an encrypted string using AES.
    """

    def __init__(self, value: Any, key: Any):
        super().__init__("AES_DECRYPT", value, key)


class AesEncrypt(Function):
    # pylint: disable=too-few-public-methods
    """
    Encrypts a string using AES.
    """

    def __init__(self, value: Any, key: Any):
        super().__init__("AES_ENCRYPT", value, key)


class Compress(Function):
    # pylint: disable=too-few-public-methods
    """
    Compress a string.
    """

    def __init__(self, value: Any):
        super().__init__("COMPRESS", value)


class DesDecrypt(Function):
    # pylint: disable=too-few-public-methods
    """
    Decrypts an encrypted string using DES.
    """

    def __init__(self, value: Any, key: Any):
        super().__init__("DES_DECRYPT", value, key)


class DesEncrypt(Function):
    # pylint: disable=too-few-public-methods
    """
    Encrypts a string using DES.
    """

    def __init__(self, value: Any, key: Any):
        super().__init__("DES_ENCRYPT", value, key)


class Encode(Function):
    # pylint: disable=too-few-public-methods
    """
    Encode a string.
    """

    def __init__(self, value: Any, encoding: str):
        super().__init__("ENCODE", value, encoding)


class Decode(Function):
    # pylint: disable=too-few-public-methods
    """
    Decode a string.
    """

    def __init__(self, value: Any, encoding: str):
        super().__init__("DECODE", value, encoding)


class Encrypt(Function):
    # pylint: disable=too-few-public-methods
    """
    Encrypt a string using Unix crypt()
    """

    def __init__(self, value: Any, salt: Any = None):
        if salt is None:
            super().__init__("ENCRYPT", value)
        else:
            super().__init__("ENCRYPT", value, salt)


class Kdf(Function):
    # pylint: disable=too-few-public-methods
    """
    Key derivation function.
    """

    def __init__(
        self,
        key: Any,
        salt: Any,
        info_or_iterations: Any = None,
        kdf_name: Optional[Literal["hkdf", "pbkdf2_hmac"] | Statement] = None,
        width: Any = None,
    ):
        args = [key, salt]

        if info_or_iterations is not None:
            args.append(info_or_iterations)

            if kdf_name is not None:
                args.append(kdf_name)

                if width is not None:
                    args.append(width)

        super().__init__("KDF", *args)


class OldPassword(Function):
    # pylint: disable=too-few-public-methods
    """
    Hash a string using the old MySQL password hashing algorithm.
    """

    def __init__(self, value: Any):
        super().__init__("OLD_PASSWORD", value)


class Password(Function):
    # pylint: disable=too-few-public-methods
    """
    Hash a string using the MySQL password hashing algorithm.
    """

    def __init__(self, value: Any):
        super().__init__("PASSWORD", value)


class MD5(Function):
    # pylint: disable=too-few-public-methods
    """
    Calculate an MD5 128-bit checksum.
    """

    def __init__(self, value: Any):
        super().__init__("MD5", value)


class RandomBytes(Function):
    # pylint: disable=too-few-public-methods
    """
    Generate a random byte string.
    """

    def __init__(self, length: Any):
        super().__init__("RANDOM_BYTES", length)


class Sha1(Function):
    # pylint: disable=too-few-public-methods
    """
    Calculate an SHA-1 160-bit checksum.
    """

    def __init__(self, value: Any):
        super().__init__("SHA1", value)


class Sha2(Function):
    # pylint: disable=too-few-public-methods
    """
    Calculate an SHA-2 checksum.
    """

    def __init__(self, value: Any, length: Any):
        super().__init__("SHA2", value, length)


class Uncompress(Function):
    # pylint: disable=too-few-public-methods
    """
    Uncompress a compressed string.
    """

    def __init__(self, value: Any):
        super().__init__("UNCOMPRESS", value)


class UncompressLength(Function):
    # pylint: disable=too-few-public-methods
    """
    Return the length of an uncompressed string.
    """

    def __init__(self, value: Any):
        super().__init__("UNCOMPRESS_LENGTH", value)
