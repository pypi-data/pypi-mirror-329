from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class DataAvailabilityHeader(_message.Message):
    __slots__ = ('row_roots', 'column_roots')
    ROW_ROOTS_FIELD_NUMBER: _ClassVar[int]
    COLUMN_ROOTS_FIELD_NUMBER: _ClassVar[int]
    row_roots: _containers.RepeatedScalarFieldContainer[bytes]
    column_roots: _containers.RepeatedScalarFieldContainer[bytes]

    def __init__(self, row_roots: _Optional[_Iterable[bytes]]=..., column_roots: _Optional[_Iterable[bytes]]=...) -> None:
        ...