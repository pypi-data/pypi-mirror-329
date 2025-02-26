from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class BlobProto(_message.Message):
    __slots__ = ('namespace_id', 'data', 'share_version', 'namespace_version', 'signer')
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SHARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_VERSION_FIELD_NUMBER: _ClassVar[int]
    SIGNER_FIELD_NUMBER: _ClassVar[int]
    namespace_id: bytes
    data: bytes
    share_version: int
    namespace_version: int
    signer: bytes

    def __init__(self, namespace_id: _Optional[bytes]=..., data: _Optional[bytes]=..., share_version: _Optional[int]=..., namespace_version: _Optional[int]=..., signer: _Optional[bytes]=...) -> None:
        ...

class BlobTx(_message.Message):
    __slots__ = ('tx', 'blobs', 'type_id')
    TX_FIELD_NUMBER: _ClassVar[int]
    BLOBS_FIELD_NUMBER: _ClassVar[int]
    TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    tx: bytes
    blobs: _containers.RepeatedCompositeFieldContainer[BlobProto]
    type_id: str

    def __init__(self, tx: _Optional[bytes]=..., blobs: _Optional[_Iterable[_Union[BlobProto, _Mapping]]]=..., type_id: _Optional[str]=...) -> None:
        ...

class IndexWrapper(_message.Message):
    __slots__ = ('tx', 'share_indexes', 'type_id')
    TX_FIELD_NUMBER: _ClassVar[int]
    SHARE_INDEXES_FIELD_NUMBER: _ClassVar[int]
    TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    tx: bytes
    share_indexes: _containers.RepeatedScalarFieldContainer[int]
    type_id: str

    def __init__(self, tx: _Optional[bytes]=..., share_indexes: _Optional[_Iterable[int]]=..., type_id: _Optional[str]=...) -> None:
        ...