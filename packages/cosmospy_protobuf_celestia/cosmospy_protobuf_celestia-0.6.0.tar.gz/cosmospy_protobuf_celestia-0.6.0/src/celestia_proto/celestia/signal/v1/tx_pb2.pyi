from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class MsgSignalVersion(_message.Message):
    __slots__ = ('validator_address', 'version')
    VALIDATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    validator_address: str
    version: int

    def __init__(self, validator_address: _Optional[str]=..., version: _Optional[int]=...) -> None:
        ...

class MsgSignalVersionResponse(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...

class MsgTryUpgrade(_message.Message):
    __slots__ = ('signer',)
    SIGNER_FIELD_NUMBER: _ClassVar[int]
    signer: str

    def __init__(self, signer: _Optional[str]=...) -> None:
        ...

class MsgTryUpgradeResponse(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...