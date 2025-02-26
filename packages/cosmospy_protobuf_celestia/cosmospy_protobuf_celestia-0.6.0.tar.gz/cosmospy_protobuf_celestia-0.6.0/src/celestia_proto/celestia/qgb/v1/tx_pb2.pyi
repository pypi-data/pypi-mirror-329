from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class MsgRegisterEVMAddress(_message.Message):
    __slots__ = ('validator_address', 'evm_address')
    VALIDATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    EVM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    validator_address: str
    evm_address: str

    def __init__(self, validator_address: _Optional[str]=..., evm_address: _Optional[str]=...) -> None:
        ...

class MsgRegisterEVMAddressResponse(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...