from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class TxStatusRequest(_message.Message):
    __slots__ = ('tx_id',)
    TX_ID_FIELD_NUMBER: _ClassVar[int]
    tx_id: str

    def __init__(self, tx_id: _Optional[str]=...) -> None:
        ...

class TxStatusResponse(_message.Message):
    __slots__ = ('height', 'index', 'execution_code', 'error', 'status')
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    height: int
    index: int
    execution_code: int
    error: str
    status: str

    def __init__(self, height: _Optional[int]=..., index: _Optional[int]=..., execution_code: _Optional[int]=..., error: _Optional[str]=..., status: _Optional[str]=...) -> None:
        ...