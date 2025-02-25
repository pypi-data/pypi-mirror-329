import hashlib

from Crypto.Hash import RIPEMD160  # type: ignore # nosec


def sha256(contents: bytes) -> bytes:
    """
    Get sha256 hash.

    :param contents: bytes contents.

    :return: bytes sha256 hash.
    """
    h = hashlib.sha256()
    h.update(contents)
    return h.digest()


def ripemd160(contents: bytes) -> bytes:
    """
    Get ripemd160 hash using PyCryptodome.

    :param contents: bytes contents.

    :return: bytes ripemd160 hash.
    """
    h = RIPEMD160.new()
    h.update(contents)
    return h.digest()
