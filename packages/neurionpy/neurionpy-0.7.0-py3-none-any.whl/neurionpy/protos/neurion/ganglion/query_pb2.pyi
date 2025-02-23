from amino import amino_pb2 as _amino_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from neurion.ganglion import params_pb2 as _params_pb2
from neurion.ganglion import ion_pb2 as _ion_pb2
from neurion.ganglion import pathway_pb2 as _pathway_pb2
from neurion.ganglion import pathway_user_pb2 as _pathway_user_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryParamsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryParamsResponse(_message.Message):
    __slots__ = ("params",)
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params
    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]] = ...) -> None: ...

class QueryIonByIonAddressRequest(_message.Message):
    __slots__ = ("ion_address",)
    ION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ion_address: str
    def __init__(self, ion_address: _Optional[str] = ...) -> None: ...

class QueryIonByIonAddressResponse(_message.Message):
    __slots__ = ("ion",)
    ION_FIELD_NUMBER: _ClassVar[int]
    ion: _ion_pb2.Ion
    def __init__(self, ion: _Optional[_Union[_ion_pb2.Ion, _Mapping]] = ...) -> None: ...

class QueryIonByCreatorRequest(_message.Message):
    __slots__ = ("creator",)
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    creator: str
    def __init__(self, creator: _Optional[str] = ...) -> None: ...

class QueryIonByCreatorResponse(_message.Message):
    __slots__ = ("ion",)
    ION_FIELD_NUMBER: _ClassVar[int]
    ion: _ion_pb2.Ion
    def __init__(self, ion: _Optional[_Union[_ion_pb2.Ion, _Mapping]] = ...) -> None: ...

class QueryGetValidatorsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryGetValidatorsResponse(_message.Message):
    __slots__ = ("validators",)
    VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    validators: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, validators: _Optional[_Iterable[str]] = ...) -> None: ...

class QueryIonsByInputSchemaHashRequest(_message.Message):
    __slots__ = ("input_schema_hash", "offset", "limit")
    INPUT_SCHEMA_HASH_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    input_schema_hash: str
    offset: int
    limit: int
    def __init__(self, input_schema_hash: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class QueryIonsByInputSchemaHashResponse(_message.Message):
    __slots__ = ("ions", "pagination")
    IONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ions: _containers.RepeatedCompositeFieldContainer[_ion_pb2.Ion]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, ions: _Optional[_Iterable[_Union[_ion_pb2.Ion, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryGetPathwayRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class QueryGetPathwayResponse(_message.Message):
    __slots__ = ("pathway",)
    PATHWAY_FIELD_NUMBER: _ClassVar[int]
    pathway: _pathway_pb2.Pathway
    def __init__(self, pathway: _Optional[_Union[_pathway_pb2.Pathway, _Mapping]] = ...) -> None: ...

class QueryListPathwaysRequest(_message.Message):
    __slots__ = ("creator", "offset", "limit")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    creator: str
    offset: int
    limit: int
    def __init__(self, creator: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class QueryListPathwaysResponse(_message.Message):
    __slots__ = ("pathways", "pagination")
    PATHWAYS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pathways: _containers.RepeatedCompositeFieldContainer[_pathway_pb2.Pathway]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, pathways: _Optional[_Iterable[_Union[_pathway_pb2.Pathway, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryListIonsByAddressesRequest(_message.Message):
    __slots__ = ("ion_addresses",)
    ION_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    ion_addresses: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ion_addresses: _Optional[_Iterable[str]] = ...) -> None: ...

class QueryListIonsByAddressesResponse(_message.Message):
    __slots__ = ("ions",)
    IONS_FIELD_NUMBER: _ClassVar[int]
    ions: _containers.RepeatedCompositeFieldContainer[_ion_pb2.Ion]
    def __init__(self, ions: _Optional[_Iterable[_Union[_ion_pb2.Ion, _Mapping]]] = ...) -> None: ...

class QueryUserPathwayStakeRequest(_message.Message):
    __slots__ = ("id", "user")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    id: int
    user: str
    def __init__(self, id: _Optional[int] = ..., user: _Optional[str] = ...) -> None: ...

class QueryUserPathwayStakeResponse(_message.Message):
    __slots__ = ("stake",)
    STAKE_FIELD_NUMBER: _ClassVar[int]
    stake: int
    def __init__(self, stake: _Optional[int] = ...) -> None: ...

class QueryGetUserRewardRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: str
    def __init__(self, user: _Optional[str] = ...) -> None: ...

class QueryGetUserRewardResponse(_message.Message):
    __slots__ = ("reward",)
    REWARD_FIELD_NUMBER: _ClassVar[int]
    reward: int
    def __init__(self, reward: _Optional[int] = ...) -> None: ...

class QueryGetProtocolFeeRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryGetProtocolFeeResponse(_message.Message):
    __slots__ = ("fee",)
    FEE_FIELD_NUMBER: _ClassVar[int]
    fee: int
    def __init__(self, fee: _Optional[int] = ...) -> None: ...

class QueryPathwaysUsingIonRequest(_message.Message):
    __slots__ = ("ion_address",)
    ION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ion_address: str
    def __init__(self, ion_address: _Optional[str] = ...) -> None: ...

class QueryPathwaysUsingIonResponse(_message.Message):
    __slots__ = ("pathways",)
    PATHWAYS_FIELD_NUMBER: _ClassVar[int]
    pathways: _containers.RepeatedCompositeFieldContainer[_pathway_pb2.Pathway]
    def __init__(self, pathways: _Optional[_Iterable[_Union[_pathway_pb2.Pathway, _Mapping]]] = ...) -> None: ...

class QueryIonsByReportsRequest(_message.Message):
    __slots__ = ("offset", "limit")
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    offset: int
    limit: int
    def __init__(self, offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class QueryIonsByReportsResponse(_message.Message):
    __slots__ = ("ion_addresses", "pagination")
    ION_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ion_addresses: _containers.RepeatedScalarFieldContainer[str]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, ion_addresses: _Optional[_Iterable[str]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryListAllPathwaysRequest(_message.Message):
    __slots__ = ("offset", "limit")
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    offset: int
    limit: int
    def __init__(self, offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class QueryListAllPathwaysResponse(_message.Message):
    __slots__ = ("pathways", "pagination")
    PATHWAYS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pathways: _containers.RepeatedCompositeFieldContainer[_pathway_pb2.Pathway]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, pathways: _Optional[_Iterable[_Union[_pathway_pb2.Pathway, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryGetRewardRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: str
    def __init__(self, user: _Optional[str] = ...) -> None: ...

class QueryGetRewardResponse(_message.Message):
    __slots__ = ("reward",)
    REWARD_FIELD_NUMBER: _ClassVar[int]
    reward: int
    def __init__(self, reward: _Optional[int] = ...) -> None: ...

class QueryGetStakeRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: str
    def __init__(self, user: _Optional[str] = ...) -> None: ...

class QueryGetStakeResponse(_message.Message):
    __slots__ = ("stake",)
    STAKE_FIELD_NUMBER: _ClassVar[int]
    stake: int
    def __init__(self, stake: _Optional[int] = ...) -> None: ...

class QueryGetIonRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class QueryGetIonResponse(_message.Message):
    __slots__ = ("ion",)
    ION_FIELD_NUMBER: _ClassVar[int]
    ion: _ion_pb2.Ion
    def __init__(self, ion: _Optional[_Union[_ion_pb2.Ion, _Mapping]] = ...) -> None: ...

class QueryGetPathwayUnstakeInitiatedUsersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryGetPathwayUnstakeInitiatedUsersResponse(_message.Message):
    __slots__ = ("pathway_users",)
    PATHWAY_USERS_FIELD_NUMBER: _ClassVar[int]
    pathway_users: _containers.RepeatedCompositeFieldContainer[_pathway_user_pb2.PathwayUser]
    def __init__(self, pathway_users: _Optional[_Iterable[_Union[_pathway_user_pb2.PathwayUser, _Mapping]]] = ...) -> None: ...

class QueryGetStakerRewardRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryGetStakerRewardResponse(_message.Message):
    __slots__ = ("reward",)
    REWARD_FIELD_NUMBER: _ClassVar[int]
    reward: int
    def __init__(self, reward: _Optional[int] = ...) -> None: ...

class QueryGetAvailableIonsRequest(_message.Message):
    __slots__ = ("offset", "limit")
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    offset: int
    limit: int
    def __init__(self, offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class QueryGetAvailableIonsResponse(_message.Message):
    __slots__ = ("ions", "pagination")
    IONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ions: _containers.RepeatedCompositeFieldContainer[_ion_pb2.Ion]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, ions: _Optional[_Iterable[_Union[_ion_pb2.Ion, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...
