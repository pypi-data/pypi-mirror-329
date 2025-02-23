import warnings
from dataclasses import dataclass
from typing import Optional, Union


class NetworkConfigError(RuntimeError):
    """Network config error.

    :param RuntimeError: Runtime error
    """


URL_PREFIXES = (
    "grpc+https",
    "grpc+http",
    "rest+https",
    "rest+http",
)


@dataclass
class NetworkConfig:
    """Network configurations.

    :raises NetworkConfigError: Network config error
    :raises RuntimeError: Runtime error
    """

    chain_id: str
    fee_minimum_gas_price: Union[int, float]
    fee_denomination: str
    staking_denomination: str
    url: str
    faucet_url: Optional[str] = None

    def validate(self):
        """Validate the network configuration.

        :raises NetworkConfigError: Network config error
        """
        if self.chain_id == "":
            raise NetworkConfigError("Chain id must be set")
        if self.url == "":
            raise NetworkConfigError("URL must be set")
        if not any(
            map(
                lambda x: self.url.startswith(  # noqa: # pylint: disable=unnecessary-lambda
                    x
                ),
                URL_PREFIXES,
            )
        ):
            prefix_list = ", ".join(map(lambda x: f'"{x}"', URL_PREFIXES))
            raise NetworkConfigError(
                f"URL must start with one of the following prefixes: {prefix_list}"
            )

    @classmethod
    def neurion_localnet(cls):
        return NetworkConfig(
            chain_id="neurion",
            url="grpc+http://0.0.0.0:9090",
            fee_minimum_gas_price=0,
            fee_denomination="union",
            staking_denomination="union",
            faucet_url=None,
        )

    @classmethod
    def neurion_alpha_testnet(cls):
        """Get the neurion alpha testnet.

        :raises RuntimeError: No alpha testnet available
        """
        raise RuntimeError("No alpha testnet available")

    @classmethod
    def neurion_beta_testnet(cls):
        """Get the neurion beta testnet.

        :raises RuntimeError: No beta testnet available
        """
        raise RuntimeError("No beta testnet available")

    @classmethod
    def neurion_stable_testnet(cls):
        """Get the neurion stable testnet.

        :return: neurion stable testnet. For now dorado is neurion stable testnet.
        """
        return cls.neurion_stable_testnet()

    @classmethod
    def neurion_mainnet(cls) -> "NetworkConfig":
        """Get the neurion mainnet configuration.

        :return: neurion mainnet configuration
        """
        return NetworkConfig(
            chain_id="neurion",
            url="grpc+https://neurion.xyz",
            fee_minimum_gas_price=0,
            fee_denomination="afet",
            staking_denomination="afet",
            faucet_url=None,
        )


    @classmethod
    def latest_stable_testnet(cls) -> "NetworkConfig":
        """Get the latest stable testnet.

        :return: latest stable testnet
        """
        warnings.warn(
            "latest_stable_testnet is deprecated, use neurion_stable_testnet instead",
            DeprecationWarning,
        )
        return cls.neurion_stable_testnet()
