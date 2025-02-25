from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class ShareProof(_message.Message):
    __slots__ = ('data', 'share_proofs', 'namespace_id', 'row_proof', 'namespace_version')
    DATA_FIELD_NUMBER: _ClassVar[int]
    SHARE_PROOFS_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_ID_FIELD_NUMBER: _ClassVar[int]
    ROW_PROOF_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_VERSION_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedScalarFieldContainer[bytes]
    share_proofs: _containers.RepeatedCompositeFieldContainer[NMTProof]
    namespace_id: bytes
    row_proof: RowProof
    namespace_version: int

    def __init__(self, data: _Optional[_Iterable[bytes]]=..., share_proofs: _Optional[_Iterable[_Union[NMTProof, _Mapping]]]=..., namespace_id: _Optional[bytes]=..., row_proof: _Optional[_Union[RowProof, _Mapping]]=..., namespace_version: _Optional[int]=...) -> None:
        ...

class RowProof(_message.Message):
    __slots__ = ('row_roots', 'proofs', 'root', 'start_row', 'end_row')
    ROW_ROOTS_FIELD_NUMBER: _ClassVar[int]
    PROOFS_FIELD_NUMBER: _ClassVar[int]
    ROOT_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    END_ROW_FIELD_NUMBER: _ClassVar[int]
    row_roots: _containers.RepeatedScalarFieldContainer[bytes]
    proofs: _containers.RepeatedCompositeFieldContainer[Proof]
    root: bytes
    start_row: int
    end_row: int

    def __init__(self, row_roots: _Optional[_Iterable[bytes]]=..., proofs: _Optional[_Iterable[_Union[Proof, _Mapping]]]=..., root: _Optional[bytes]=..., start_row: _Optional[int]=..., end_row: _Optional[int]=...) -> None:
        ...

class NMTProof(_message.Message):
    __slots__ = ('start', 'end', 'nodes', 'leaf_hash')
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    LEAF_HASH_FIELD_NUMBER: _ClassVar[int]
    start: int
    end: int
    nodes: _containers.RepeatedScalarFieldContainer[bytes]
    leaf_hash: bytes

    def __init__(self, start: _Optional[int]=..., end: _Optional[int]=..., nodes: _Optional[_Iterable[bytes]]=..., leaf_hash: _Optional[bytes]=...) -> None:
        ...

class Proof(_message.Message):
    __slots__ = ('total', 'index', 'leaf_hash', 'aunts')
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    LEAF_HASH_FIELD_NUMBER: _ClassVar[int]
    AUNTS_FIELD_NUMBER: _ClassVar[int]
    total: int
    index: int
    leaf_hash: bytes
    aunts: _containers.RepeatedScalarFieldContainer[bytes]

    def __init__(self, total: _Optional[int]=..., index: _Optional[int]=..., leaf_hash: _Optional[bytes]=..., aunts: _Optional[_Iterable[bytes]]=...) -> None:
        ...