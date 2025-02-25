"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'celestia/core/v1/proof/proof.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n"celestia/core/v1/proof/proof.proto\x12\x16celestia.core.v1.proof"\xb8\x01\n\nShareProof\x12\x0c\n\x04data\x18\x01 \x03(\x0c\x126\n\x0cshare_proofs\x18\x02 \x03(\x0b2 .celestia.core.v1.proof.NMTProof\x12\x14\n\x0cnamespace_id\x18\x03 \x01(\x0c\x123\n\trow_proof\x18\x04 \x01(\x0b2 .celestia.core.v1.proof.RowProof\x12\x19\n\x11namespace_version\x18\x05 \x01(\r"~\n\x08RowProof\x12\x11\n\trow_roots\x18\x01 \x03(\x0c\x12-\n\x06proofs\x18\x02 \x03(\x0b2\x1d.celestia.core.v1.proof.Proof\x12\x0c\n\x04root\x18\x03 \x01(\x0c\x12\x11\n\tstart_row\x18\x04 \x01(\r\x12\x0f\n\x07end_row\x18\x05 \x01(\r"H\n\x08NMTProof\x12\r\n\x05start\x18\x01 \x01(\x05\x12\x0b\n\x03end\x18\x02 \x01(\x05\x12\r\n\x05nodes\x18\x03 \x03(\x0c\x12\x11\n\tleaf_hash\x18\x04 \x01(\x0c"G\n\x05Proof\x12\r\n\x05total\x18\x01 \x01(\x03\x12\r\n\x05index\x18\x02 \x01(\x03\x12\x11\n\tleaf_hash\x18\x03 \x01(\x0c\x12\r\n\x05aunts\x18\x04 \x03(\x0cB/Z-github.com/celestiaorg/celestia-app/pkg/proofb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'celestia.core.v1.proof.proof_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z-github.com/celestiaorg/celestia-app/pkg/proof'
    _globals['_SHAREPROOF']._serialized_start = 63
    _globals['_SHAREPROOF']._serialized_end = 247
    _globals['_ROWPROOF']._serialized_start = 249
    _globals['_ROWPROOF']._serialized_end = 375
    _globals['_NMTPROOF']._serialized_start = 377
    _globals['_NMTPROOF']._serialized_end = 449
    _globals['_PROOF']._serialized_start = 451
    _globals['_PROOF']._serialized_end = 522