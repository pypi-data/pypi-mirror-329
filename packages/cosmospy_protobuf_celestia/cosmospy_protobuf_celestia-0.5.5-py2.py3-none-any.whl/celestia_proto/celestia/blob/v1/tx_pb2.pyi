from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class MsgPayForBlobs(_message.Message):
    __slots__ = ('signer', 'namespaces', 'blob_sizes', 'share_commitments', 'share_versions')
    SIGNER_FIELD_NUMBER: _ClassVar[int]
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    BLOB_SIZES_FIELD_NUMBER: _ClassVar[int]
    SHARE_COMMITMENTS_FIELD_NUMBER: _ClassVar[int]
    SHARE_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    signer: str
    namespaces: _containers.RepeatedScalarFieldContainer[bytes]
    blob_sizes: _containers.RepeatedScalarFieldContainer[int]
    share_commitments: _containers.RepeatedScalarFieldContainer[bytes]
    share_versions: _containers.RepeatedScalarFieldContainer[int]

    def __init__(self, signer: _Optional[str]=..., namespaces: _Optional[_Iterable[bytes]]=..., blob_sizes: _Optional[_Iterable[int]]=..., share_commitments: _Optional[_Iterable[bytes]]=..., share_versions: _Optional[_Iterable[int]]=...) -> None:
        ...

class MsgPayForBlobsResponse(_message.Message):
    __slots__ = ()

    def __init__(self) -> None:
        ...