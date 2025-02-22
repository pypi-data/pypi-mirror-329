from amino import amino_pb2 as _amino_pb2
from cosmos.msg.v1 import msg_pb2 as _msg_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from neurion.ganglion import ion_pb2 as _ion_pb2
from neurion.ganglion import params_pb2 as _params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgUpdateParams(_message.Message):
    __slots__ = ("authority", "params")
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    authority: str
    params: _params_pb2.Params
    def __init__(self, authority: _Optional[str] = ..., params: _Optional[_Union[_params_pb2.Params, _Mapping]] = ...) -> None: ...

class MsgUpdateParamsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgRegisterIon(_message.Message):
    __slots__ = ("creator", "capacities", "stake", "endpoints", "description", "input_schema", "output_schema", "fee_per_thousand_calls")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    CAPACITIES_FIELD_NUMBER: _ClassVar[int]
    STAKE_FIELD_NUMBER: _ClassVar[int]
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    INPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    FEE_PER_THOUSAND_CALLS_FIELD_NUMBER: _ClassVar[int]
    creator: str
    capacities: _containers.RepeatedScalarFieldContainer[str]
    stake: int
    endpoints: _containers.RepeatedScalarFieldContainer[str]
    description: str
    input_schema: str
    output_schema: str
    fee_per_thousand_calls: int
    def __init__(self, creator: _Optional[str] = ..., capacities: _Optional[_Iterable[str]] = ..., stake: _Optional[int] = ..., endpoints: _Optional[_Iterable[str]] = ..., description: _Optional[str] = ..., input_schema: _Optional[str] = ..., output_schema: _Optional[str] = ..., fee_per_thousand_calls: _Optional[int] = ...) -> None: ...

class MsgRegisterIonResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgReportUnavailableIon(_message.Message):
    __slots__ = ("creator", "ion_address")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    ION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    creator: str
    ion_address: str
    def __init__(self, creator: _Optional[str] = ..., ion_address: _Optional[str] = ...) -> None: ...

class MsgReportUnavailableIonResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgUnreportUnavailableIon(_message.Message):
    __slots__ = ("creator", "ion_address")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    ION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    creator: str
    ion_address: str
    def __init__(self, creator: _Optional[str] = ..., ion_address: _Optional[str] = ...) -> None: ...

class MsgUnreportUnavailableIonResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgAddValidator(_message.Message):
    __slots__ = ("creator", "validator_address")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    creator: str
    validator_address: str
    def __init__(self, creator: _Optional[str] = ..., validator_address: _Optional[str] = ...) -> None: ...

class MsgAddValidatorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgRemoveValidator(_message.Message):
    __slots__ = ("creator", "validator_address")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    creator: str
    validator_address: str
    def __init__(self, creator: _Optional[str] = ..., validator_address: _Optional[str] = ...) -> None: ...

class MsgRemoveValidatorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgValidateAvailability(_message.Message):
    __slots__ = ("creator", "ion_address", "available")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    ION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    creator: str
    ion_address: str
    available: bool
    def __init__(self, creator: _Optional[str] = ..., ion_address: _Optional[str] = ..., available: bool = ...) -> None: ...

class MsgValidateAvailabilityResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class MsgRegisterPathway(_message.Message):
    __slots__ = ("creator", "name", "description", "is_public", "ions", "field_maps_base64")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLIC_FIELD_NUMBER: _ClassVar[int]
    IONS_FIELD_NUMBER: _ClassVar[int]
    FIELD_MAPS_BASE64_FIELD_NUMBER: _ClassVar[int]
    creator: str
    name: str
    description: str
    is_public: bool
    ions: _containers.RepeatedScalarFieldContainer[str]
    field_maps_base64: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, creator: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_public: bool = ..., ions: _Optional[_Iterable[str]] = ..., field_maps_base64: _Optional[_Iterable[str]] = ...) -> None: ...

class MsgRegisterPathwayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgStakePathway(_message.Message):
    __slots__ = ("creator", "id", "amount")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    creator: str
    id: int
    amount: int
    def __init__(self, creator: _Optional[str] = ..., id: _Optional[int] = ..., amount: _Optional[int] = ...) -> None: ...

class MsgStakePathwayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgRefundPathwayStake(_message.Message):
    __slots__ = ("creator", "id", "user", "num_calls")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    NUM_CALLS_FIELD_NUMBER: _ClassVar[int]
    creator: str
    id: int
    user: str
    num_calls: int
    def __init__(self, creator: _Optional[str] = ..., id: _Optional[int] = ..., user: _Optional[str] = ..., num_calls: _Optional[int] = ...) -> None: ...

class MsgRefundPathwayStakeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgInitUnstakePathway(_message.Message):
    __slots__ = ("creator", "id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    id: int
    def __init__(self, creator: _Optional[str] = ..., id: _Optional[int] = ...) -> None: ...

class MsgInitUnstakePathwayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgClaimProtocolFee(_message.Message):
    __slots__ = ("creator",)
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    creator: str
    def __init__(self, creator: _Optional[str] = ...) -> None: ...

class MsgClaimProtocolFeeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgSettlePathwayStake(_message.Message):
    __slots__ = ("creator", "id", "user", "num_calls")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    NUM_CALLS_FIELD_NUMBER: _ClassVar[int]
    creator: str
    id: int
    user: str
    num_calls: int
    def __init__(self, creator: _Optional[str] = ..., id: _Optional[int] = ..., user: _Optional[str] = ..., num_calls: _Optional[int] = ...) -> None: ...

class MsgSettlePathwayStakeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgStakeToGanglion(_message.Message):
    __slots__ = ("creator", "amount")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    creator: str
    amount: int
    def __init__(self, creator: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...

class MsgStakeToGanglionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgClaimReward(_message.Message):
    __slots__ = ("creator",)
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    creator: str
    def __init__(self, creator: _Optional[str] = ...) -> None: ...

class MsgClaimRewardResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgUnstakeFromGanglion(_message.Message):
    __slots__ = ("creator", "amount")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    creator: str
    amount: int
    def __init__(self, creator: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...

class MsgUnstakeFromGanglionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgUpdatePathway(_message.Message):
    __slots__ = ("creator", "id", "name", "description", "is_public", "ions", "field_maps_base64")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLIC_FIELD_NUMBER: _ClassVar[int]
    IONS_FIELD_NUMBER: _ClassVar[int]
    FIELD_MAPS_BASE64_FIELD_NUMBER: _ClassVar[int]
    creator: str
    id: int
    name: str
    description: str
    is_public: bool
    ions: _containers.RepeatedScalarFieldContainer[str]
    field_maps_base64: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, creator: _Optional[str] = ..., id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_public: bool = ..., ions: _Optional[_Iterable[str]] = ..., field_maps_base64: _Optional[_Iterable[str]] = ...) -> None: ...

class MsgUpdatePathwayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
