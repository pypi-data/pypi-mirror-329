# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: plume/sample/unity/xritk/xr_base_interactable.proto
# Protobuf Python Version: 5.29.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    3,
    '',
    'plume/sample/unity/xritk/xr_base_interactable.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from plume.sample.unity import identifiers_pb2 as plume_dot_sample_dot_unity_dot_identifiers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3plume/sample/unity/xritk/xr_base_interactable.proto\x12\x18plume.sample.unity.xritk\x1a$plume/sample/unity/identifiers.proto\"a\n\x18XRBaseInteractableCreate\x12\x45\n\tcomponent\x18\x01 \x01(\x0b\x32\'.plume.sample.unity.ComponentIdentifierR\tcomponent\"b\n\x19XRBaseInteractableDestroy\x12\x45\n\tcomponent\x18\x01 \x01(\x0b\x32\'.plume.sample.unity.ComponentIdentifierR\tcomponent\"\x8c\x01\n\x18XRBaseInteractableUpdate\x12\x45\n\tcomponent\x18\x01 \x01(\x0b\x32\'.plume.sample.unity.ComponentIdentifierR\tcomponent\x12\x1d\n\x07\x65nabled\x18\x02 \x01(\x08H\x00R\x07\x65nabled\x88\x01\x01\x42\n\n\x08_enabledB\x1b\xaa\x02\x18PLUME.Sample.Unity.XRITKb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'plume.sample.unity.xritk.xr_base_interactable_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\252\002\030PLUME.Sample.Unity.XRITK'
  _globals['_XRBASEINTERACTABLECREATE']._serialized_start=119
  _globals['_XRBASEINTERACTABLECREATE']._serialized_end=216
  _globals['_XRBASEINTERACTABLEDESTROY']._serialized_start=218
  _globals['_XRBASEINTERACTABLEDESTROY']._serialized_end=316
  _globals['_XRBASEINTERACTABLEUPDATE']._serialized_start=319
  _globals['_XRBASEINTERACTABLEUPDATE']._serialized_end=459
# @@protoc_insertion_point(module_scope)
