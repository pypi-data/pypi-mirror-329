from amino import amino_pb2 as _amino_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from neurion.sanctum import params_pb2 as _params_pb2
from neurion.sanctum import dataset_application_pb2 as _dataset_application_pb2
from neurion.sanctum import dataset_usage_request_pb2 as _dataset_usage_request_pb2
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

class QueryGetAvailableDatasetsRequest(_message.Message):
    __slots__ = ("offset", "limit")
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    offset: int
    limit: int
    def __init__(self, offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class QueryGetAvailableDatasetsResponse(_message.Message):
    __slots__ = ("datasets", "pagination")
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    datasets: _containers.RepeatedCompositeFieldContainer[_dataset_application_pb2.DatasetApplication]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, datasets: _Optional[_Iterable[_Union[_dataset_application_pb2.DatasetApplication, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryGetApprovedUsageRequestsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryGetApprovedUsageRequestsResponse(_message.Message):
    __slots__ = ("requests",)
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[_dataset_usage_request_pb2.DatasetUsageRequest]
    def __init__(self, requests: _Optional[_Iterable[_Union[_dataset_usage_request_pb2.DatasetUsageRequest, _Mapping]]] = ...) -> None: ...

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

class QueryGetPendingDatasetsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryGetPendingDatasetsResponse(_message.Message):
    __slots__ = ("datasets",)
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    datasets: _containers.RepeatedCompositeFieldContainer[_dataset_application_pb2.DatasetApplication]
    def __init__(self, datasets: _Optional[_Iterable[_Union[_dataset_application_pb2.DatasetApplication, _Mapping]]] = ...) -> None: ...

class QueryGetPendingUsageRequestsRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: str
    def __init__(self, user: _Optional[str] = ...) -> None: ...

class QueryGetPendingUsageRequestsResponse(_message.Message):
    __slots__ = ("requests",)
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[_dataset_usage_request_pb2.DatasetUsageRequest]
    def __init__(self, requests: _Optional[_Iterable[_Union[_dataset_usage_request_pb2.DatasetUsageRequest, _Mapping]]] = ...) -> None: ...

class QueryGetDatasetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class QueryGetDatasetResponse(_message.Message):
    __slots__ = ("dataset",)
    DATASET_FIELD_NUMBER: _ClassVar[int]
    dataset: _dataset_application_pb2.DatasetApplication
    def __init__(self, dataset: _Optional[_Union[_dataset_application_pb2.DatasetApplication, _Mapping]] = ...) -> None: ...

class QueryGetUsageRequestRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class QueryGetUsageRequestResponse(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _dataset_usage_request_pb2.DatasetUsageRequest
    def __init__(self, request: _Optional[_Union[_dataset_usage_request_pb2.DatasetUsageRequest, _Mapping]] = ...) -> None: ...

class QueryGetUsageRequestsForDatasetRequest(_message.Message):
    __slots__ = ("dataset_id", "offset", "limit")
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    dataset_id: int
    offset: int
    limit: int
    def __init__(self, dataset_id: _Optional[int] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class QueryGetUsageRequestsForDatasetResponse(_message.Message):
    __slots__ = ("requests", "pagination")
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[_dataset_usage_request_pb2.DatasetUsageRequest]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, requests: _Optional[_Iterable[_Union[_dataset_usage_request_pb2.DatasetUsageRequest, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryGetUsageRequestsForUserRequest(_message.Message):
    __slots__ = ("user", "offset", "limit")
    USER_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    user: str
    offset: int
    limit: int
    def __init__(self, user: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class QueryGetUsageRequestsForUserResponse(_message.Message):
    __slots__ = ("requests", "pagination")
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[_dataset_usage_request_pb2.DatasetUsageRequest]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, requests: _Optional[_Iterable[_Union[_dataset_usage_request_pb2.DatasetUsageRequest, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryGetDatasetsForUserRequest(_message.Message):
    __slots__ = ("user", "offset", "limit")
    USER_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    user: str
    offset: int
    limit: int
    def __init__(self, user: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class QueryGetDatasetsForUserResponse(_message.Message):
    __slots__ = ("datasets", "pagination")
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    datasets: _containers.RepeatedCompositeFieldContainer[_dataset_application_pb2.DatasetApplication]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, datasets: _Optional[_Iterable[_Union[_dataset_application_pb2.DatasetApplication, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...
