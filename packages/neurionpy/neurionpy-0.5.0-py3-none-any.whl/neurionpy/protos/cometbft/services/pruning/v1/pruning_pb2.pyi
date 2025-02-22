from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetBlockRetainHeightRequest(_message.Message):
    __slots__ = ("height",)
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int
    def __init__(self, height: _Optional[int] = ...) -> None: ...

class SetBlockRetainHeightResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBlockRetainHeightRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBlockRetainHeightResponse(_message.Message):
    __slots__ = ("app_retain_height", "pruning_service_retain_height")
    APP_RETAIN_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    PRUNING_SERVICE_RETAIN_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    app_retain_height: int
    pruning_service_retain_height: int
    def __init__(self, app_retain_height: _Optional[int] = ..., pruning_service_retain_height: _Optional[int] = ...) -> None: ...

class SetBlockResultsRetainHeightRequest(_message.Message):
    __slots__ = ("height",)
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int
    def __init__(self, height: _Optional[int] = ...) -> None: ...

class SetBlockResultsRetainHeightResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBlockResultsRetainHeightRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBlockResultsRetainHeightResponse(_message.Message):
    __slots__ = ("pruning_service_retain_height",)
    PRUNING_SERVICE_RETAIN_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    pruning_service_retain_height: int
    def __init__(self, pruning_service_retain_height: _Optional[int] = ...) -> None: ...

class SetTxIndexerRetainHeightRequest(_message.Message):
    __slots__ = ("height",)
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int
    def __init__(self, height: _Optional[int] = ...) -> None: ...

class SetTxIndexerRetainHeightResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTxIndexerRetainHeightRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTxIndexerRetainHeightResponse(_message.Message):
    __slots__ = ("height",)
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int
    def __init__(self, height: _Optional[int] = ...) -> None: ...

class SetBlockIndexerRetainHeightRequest(_message.Message):
    __slots__ = ("height",)
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int
    def __init__(self, height: _Optional[int] = ...) -> None: ...

class SetBlockIndexerRetainHeightResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBlockIndexerRetainHeightRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBlockIndexerRetainHeightResponse(_message.Message):
    __slots__ = ("height",)
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int
    def __init__(self, height: _Optional[int] = ...) -> None: ...
