from abc import ABC, abstractmethod


class Signer(ABC):
    """Signer abstract class."""

    @abstractmethod
    def sign(
        self, message: bytes, deterministic: bool = False, canonicalise: bool = True
    ) -> bytes:
        """
        Perform signing.

        :param message: bytes to sign
        :param deterministic: bool, default false
        :param canonicalise: bool,default True
        """

    @abstractmethod
    def sign_digest(
        self, digest: bytes, deterministic=False, canonicalise: bool = True
    ) -> bytes:
        """
        Perform digest signing.

        :param digest: bytes to sign
        :param deterministic: bool, default false
        :param canonicalise: bool,default True
        """
