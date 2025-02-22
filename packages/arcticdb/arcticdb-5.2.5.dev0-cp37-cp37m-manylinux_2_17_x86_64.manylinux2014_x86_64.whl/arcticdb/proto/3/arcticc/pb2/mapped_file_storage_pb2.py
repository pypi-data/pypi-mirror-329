# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: arcticc/pb2/mapped_file_storage.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from arcticc.pb2 import encoding_pb2 as arcticc_dot_pb2_dot_encoding__pb2
from arcticc.pb2 import descriptors_pb2 as arcticc_dot_pb2_dot_descriptors__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='arcticc/pb2/mapped_file_storage.proto',
  package='arcticc.pb2.mapped_file_storage_pb2',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n%arcticc/pb2/mapped_file_storage.proto\x12#arcticc.pb2.mapped_file_storage_pb2\x1a\x1a\x61rcticc/pb2/encoding.proto\x1a\x1d\x61rcticc/pb2/descriptors.proto\"\xf7\x01\n\x06\x43onfig\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\r\n\x05\x62ytes\x18\x02 \x01(\x04\x12\x13\n\x0bitems_count\x18\x03 \x01(\x04\x12\x18\n\x10\x65ncoding_version\x18\x04 \x01(\r\x12\x10\n\x06num_id\x18\x05 \x01(\x04H\x00\x12\x10\n\x06str_id\x18\x06 \x01(\tH\x00\x12;\n\x05index\x18\x07 \x01(\x0b\x32,.arcticc.pb2.descriptors_pb2.IndexDescriptor\x12:\n\ncodec_opts\x18\x08 \x01(\x0b\x32&.arcticc.pb2.encoding_pb2.VariantCodecB\x04\n\x02idb\x06proto3'
  ,
  dependencies=[arcticc_dot_pb2_dot_encoding__pb2.DESCRIPTOR,arcticc_dot_pb2_dot_descriptors__pb2.DESCRIPTOR,])




_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='arcticc.pb2.mapped_file_storage_pb2.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='arcticc.pb2.mapped_file_storage_pb2.Config.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bytes', full_name='arcticc.pb2.mapped_file_storage_pb2.Config.bytes', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='items_count', full_name='arcticc.pb2.mapped_file_storage_pb2.Config.items_count', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='encoding_version', full_name='arcticc.pb2.mapped_file_storage_pb2.Config.encoding_version', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='num_id', full_name='arcticc.pb2.mapped_file_storage_pb2.Config.num_id', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='str_id', full_name='arcticc.pb2.mapped_file_storage_pb2.Config.str_id', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='index', full_name='arcticc.pb2.mapped_file_storage_pb2.Config.index', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='codec_opts', full_name='arcticc.pb2.mapped_file_storage_pb2.Config.codec_opts', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='id', full_name='arcticc.pb2.mapped_file_storage_pb2.Config.id',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=138,
  serialized_end=385,
)

_CONFIG.fields_by_name['index'].message_type = arcticc_dot_pb2_dot_descriptors__pb2._INDEXDESCRIPTOR
_CONFIG.fields_by_name['codec_opts'].message_type = arcticc_dot_pb2_dot_encoding__pb2._VARIANTCODEC
_CONFIG.oneofs_by_name['id'].fields.append(
  _CONFIG.fields_by_name['num_id'])
_CONFIG.fields_by_name['num_id'].containing_oneof = _CONFIG.oneofs_by_name['id']
_CONFIG.oneofs_by_name['id'].fields.append(
  _CONFIG.fields_by_name['str_id'])
_CONFIG.fields_by_name['str_id'].containing_oneof = _CONFIG.oneofs_by_name['id']
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'arcticc.pb2.mapped_file_storage_pb2'
  # @@protoc_insertion_point(class_scope:arcticc.pb2.mapped_file_storage_pb2.Config)
  })
_sym_db.RegisterMessage(Config)


# @@protoc_insertion_point(module_scope)
