# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: NNCProperties.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import Case_pb2 as Case__pb2
import Definitions_pb2 as Definitions__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13NNCProperties.proto\x12\x04rips\x1a\nCase.proto\x1a\x11\x44\x65\x66initions.proto\"R\n\x14\x41vailableNNCProperty\x12\x0c\n\x04name\x18\x01 \x01(\t\x12,\n\rproperty_type\x18\x02 \x01(\x0e\x32\x15.rips.NNCPropertyType\"H\n\x16\x41vailableNNCProperties\x12.\n\nproperties\x18\x01 \x03(\x0b\x32\x1a.rips.AvailableNNCProperty\"{\n\rNNCConnection\x12\x18\n\x10\x63\x65ll_grid_index1\x18\x01 \x01(\x05\x12\x18\n\x10\x63\x65ll_grid_index2\x18\x02 \x01(\x05\x12\x1a\n\x05\x63\x65ll1\x18\x03 \x01(\x0b\x32\x0b.rips.Vec3i\x12\x1a\n\x05\x63\x65ll2\x18\x04 \x01(\x0b\x32\x0b.rips.Vec3i\":\n\x0eNNCConnections\x12(\n\x0b\x63onnections\x18\x01 \x03(\x0b\x32\x13.rips.NNCConnection\"{\n\x10NNCValuesRequest\x12\x0f\n\x07\x63\x61se_id\x18\x01 \x01(\x05\x12\x15\n\rproperty_name\x18\x02 \x01(\t\x12,\n\rproperty_type\x18\x03 \x01(\x0e\x32\x15.rips.NNCPropertyType\x12\x11\n\ttime_step\x18\x04 \x01(\x05\"\x1b\n\tNNCValues\x12\x0e\n\x06values\x18\x01 \x03(\x01\"\x83\x01\n\x15NNCValuesInputRequest\x12\x0f\n\x07\x63\x61se_id\x18\x01 \x01(\x05\x12\x15\n\rproperty_name\x18\x02 \x01(\t\x12/\n\x0eporosity_model\x18\x03 \x01(\x0e\x32\x17.rips.PorosityModelType\x12\x11\n\ttime_step\x18\x04 \x01(\x05\"o\n\x0eNNCValuesChunk\x12-\n\x06params\x18\x01 \x01(\x0b\x32\x1b.rips.NNCValuesInputRequestH\x00\x12!\n\x06values\x18\x02 \x01(\x0b\x32\x0f.rips.NNCValuesH\x00\x42\x0b\n\tChunkType*E\n\x0fNNCPropertyType\x12\x0f\n\x0bNNC_DYNAMIC\x10\x00\x12\x0e\n\nNNC_STATIC\x10\x01\x12\x11\n\rNNC_GENERATED\x10\x02\x32\xa9\x02\n\rNNCProperties\x12N\n\x19GetAvailableNNCProperties\x12\x11.rips.CaseRequest\x1a\x1c.rips.AvailableNNCProperties\"\x00\x12@\n\x11GetNNCConnections\x12\x11.rips.CaseRequest\x1a\x14.rips.NNCConnections\"\x00\x30\x01\x12;\n\x0cGetNNCValues\x12\x16.rips.NNCValuesRequest\x1a\x0f.rips.NNCValues\"\x00\x30\x01\x12I\n\x0cSetNNCValues\x12\x14.rips.NNCValuesChunk\x1a\x1f.rips.ClientToServerStreamReply\"\x00(\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'NNCProperties_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_NNCPROPERTYTYPE']._serialized_start=804
  _globals['_NNCPROPERTYTYPE']._serialized_end=873
  _globals['_AVAILABLENNCPROPERTY']._serialized_start=60
  _globals['_AVAILABLENNCPROPERTY']._serialized_end=142
  _globals['_AVAILABLENNCPROPERTIES']._serialized_start=144
  _globals['_AVAILABLENNCPROPERTIES']._serialized_end=216
  _globals['_NNCCONNECTION']._serialized_start=218
  _globals['_NNCCONNECTION']._serialized_end=341
  _globals['_NNCCONNECTIONS']._serialized_start=343
  _globals['_NNCCONNECTIONS']._serialized_end=401
  _globals['_NNCVALUESREQUEST']._serialized_start=403
  _globals['_NNCVALUESREQUEST']._serialized_end=526
  _globals['_NNCVALUES']._serialized_start=528
  _globals['_NNCVALUES']._serialized_end=555
  _globals['_NNCVALUESINPUTREQUEST']._serialized_start=558
  _globals['_NNCVALUESINPUTREQUEST']._serialized_end=689
  _globals['_NNCVALUESCHUNK']._serialized_start=691
  _globals['_NNCVALUESCHUNK']._serialized_end=802
  _globals['_NNCPROPERTIES']._serialized_start=876
  _globals['_NNCPROPERTIES']._serialized_end=1173
# @@protoc_insertion_point(module_scope)
