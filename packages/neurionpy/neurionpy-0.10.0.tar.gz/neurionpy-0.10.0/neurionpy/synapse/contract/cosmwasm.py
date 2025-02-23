import gzip
from typing import Any, Optional

from neurionpy.synapse.coins import parse_coins
from neurionpy.common.utils import json_encode
from neurionpy.crypto.address import Address
from neurionpy.protos.cosmwasm.wasm.v1.tx_pb2 import (
    MsgClearAdmin,
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgMigrateContract,
    MsgStoreCode,
    MsgUpdateAdmin,
)


def create_cosmwasm_store_code_msg(
    contract_path: str, sender_address: Address
) -> MsgStoreCode:
    """Create cosmwasm store code message.

    :param contract_path: contract path
    :param sender_address: sender address
    :return: cosmwasm store code message
    """
    with open(contract_path, "rb") as contract_file:
        wasm_byte_code = gzip.compress(contract_file.read(), 9)

    msg = MsgStoreCode(
        sender=str(sender_address),
        wasm_byte_code=wasm_byte_code,
    )

    return msg


def create_cosmwasm_instantiate_msg(
    code_id: int,
    args: Any,
    label: str,
    sender_address: Address,
    funds: Optional[str] = None,
    admin_address: Optional[Address] = None,
) -> MsgInstantiateContract:
    """Create cosmwasm instantiate message.

    :param code_id: code id
    :param args: args
    :param label: label
    :param sender_address: sender address
    :param funds: funds, defaults to None
    :param admin_address: admin address, defaults to None
    :return: cosmwasm instantiate message
    """
    msg = MsgInstantiateContract(
        sender=str(sender_address),
        code_id=code_id,
        msg=json_encode(args).encode("UTF8"),
        label=label,
    )

    if funds is not None:
        msg.funds.extend(parse_coins(funds))
    if admin_address is not None:
        msg.admin = str(admin_address)  # noqa

    return msg


def create_cosmwasm_migrate_msg(
    code_id: int,
    args: Any,
    contract_address: Address,
    sender_address: Address,
) -> MsgMigrateContract:
    """Create cosmwasm migrate message.

    :param code_id: code id
    :param args: args
    :param contract_address: sender address
    :param sender_address: sender address
    :return: cosmwasm migrate message
    """
    msg = MsgMigrateContract(
        sender=str(sender_address),
        code_id=code_id,
        msg=json_encode(args).encode("UTF8"),
        contract=str(contract_address),
    )

    return msg


def create_cosmwasm_execute_msg(
    sender_address: Address,
    contract_address: Address,
    args: Any,
    funds: Optional[str] = None,
) -> MsgExecuteContract:
    """Create cosmwasm execute message.

    :param sender_address: sender address
    :param contract_address: contract address
    :param args: args
    :param funds: funds, defaults to None
    :return: cosmwasm execute message
    """
    msg = MsgExecuteContract(
        sender=str(sender_address),
        contract=str(contract_address),
        msg=json_encode(args).encode("UTF8"),
    )
    if funds is not None:
        msg.funds.extend(parse_coins(funds))

    return msg


def create_cosmwasm_update_admin_msg(
    sender_address: Address,
    contract_address: Address,
    new_admin: Address,
) -> MsgExecuteContract:
    """Create cosmwasm update admin message.

    :param sender_address: sender address
    :param contract_address: contract address
    :param sender_address: sender address
    :param new_admin: new admin address
    :return: cosmwasm update admin message
    """
    msg = MsgUpdateAdmin(
        sender=str(sender_address),
        contract=str(contract_address),
        new_admin=str(new_admin),
    )

    return msg


def create_cosmwasm_clear_admin_msg(
    sender_address: Address,
    contract_address: Address,
) -> MsgExecuteContract:
    """Create cosmwasm clear admin message.

    :param sender_address: sender address
    :param contract_address: contract address
    :param sender_address: sender address
    :return: cosmwasm clear admin message
    """
    msg = MsgClearAdmin(
        sender=str(sender_address),
        contract=str(contract_address),
    )

    return msg
