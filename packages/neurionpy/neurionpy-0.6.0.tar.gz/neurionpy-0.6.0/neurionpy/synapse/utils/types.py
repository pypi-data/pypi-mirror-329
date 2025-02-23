from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from google.protobuf.timestamp_pb2 import Timestamp
from neurionpy.synapse.client.staking import (
    ValidatorStatus,
)
from neurionpy.crypto.address import Address
from neurionpy.crypto.hashfuncs import sha256
from neurionpy.protos.cosmos.crypto.ed25519.keys_pb2 import (  # noqa # pylint: disable=unused-import
    PubKey,
)



DEFAULT_QUERY_TIMEOUT_SECS = 15
DEFAULT_QUERY_INTERVAL_SECS = 2
COSMOS_SDK_DEC_COIN_PRECISION = 10 ** 18


@dataclass
class Account:
    """Account."""

    address: Address
    number: int
    sequence: int


@dataclass
class StakingPosition:
    """Staking positions."""

    validator: Address
    amount: int
    reward: int


@dataclass
class UnbondingPositions:
    """Unbonding positions."""

    validator: Address
    amount: int


@dataclass
class Validator:
    """Validator."""

    address: Address  # the operators address
    tokens: int  # The total amount of tokens for the validator
    moniker: str
    status: ValidatorStatus


@dataclass
class Coin:
    """Coins."""

    amount: int
    denom: str


@dataclass
class StakingSummary:
    """Get the staking summary."""

    current_positions: List[StakingPosition]
    unbonding_positions: List[UnbondingPositions]

    @property
    def total_staked(self) -> int:
        """Get the total staked amount."""
        return sum(map(lambda p: p.amount, self.current_positions))

    @property
    def total_rewards(self) -> int:
        """Get the total rewards."""
        return sum(map(lambda p: p.reward, self.current_positions))

    @property
    def total_unbonding(self) -> int:
        """total unbonding."""
        return sum(map(lambda p: p.amount, self.unbonding_positions))


@dataclass
class Block:
    """Block."""

    height: int
    time: datetime
    chain_id: str
    tx_hashes: List[str]

    @staticmethod
    def from_proto(block: Any) -> "Block":
        """Parse the block.

        :param block: block as Any
        :return: parsed block as Block
        """
        return Block(
            height=int(block.header.height),
            time=Block._parse_timestamp(block.header.time),
            tx_hashes=[sha256(tx).hex().upper() for tx in block.data.txs],
            chain_id=block.header.chain_id,
        )

    @staticmethod
    def _parse_timestamp(timestamp: Timestamp):
        """Parse the timestamp.

        :param timestamp: timestamp
        :return: parsed timestamp
        """
        return datetime.fromtimestamp(timestamp.seconds, tz=timezone.utc) + timedelta(
            microseconds=timestamp.nanos // 1000
        )

