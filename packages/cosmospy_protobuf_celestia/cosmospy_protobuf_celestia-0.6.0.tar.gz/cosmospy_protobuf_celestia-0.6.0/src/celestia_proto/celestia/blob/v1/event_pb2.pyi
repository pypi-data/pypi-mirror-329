from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class EventPayForBlobs(_message.Message):
    __slots__ = ('signer', 'blob_sizes', 'namespaces')
    SIGNER_FIELD_NUMBER: _ClassVar[int]
    BLOB_SIZES_FIELD_NUMBER: _ClassVar[int]
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    signer: str
    blob_sizes: _containers.RepeatedScalarFieldContainer[int]
    namespaces: _containers.RepeatedScalarFieldContainer[bytes]

    def __init__(self, signer: _Optional[str]=..., blob_sizes: _Optional[_Iterable[int]]=..., namespaces: _Optional[_Iterable[bytes]]=...) -> None:
        ...