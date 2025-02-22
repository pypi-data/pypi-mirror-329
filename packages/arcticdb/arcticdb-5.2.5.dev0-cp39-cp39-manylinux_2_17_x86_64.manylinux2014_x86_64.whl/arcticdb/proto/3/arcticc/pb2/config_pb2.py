# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: arcticc/pb2/config.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='arcticc/pb2/config.proto',
  package='arcticc.pb2.config_pb2',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x18\x61rcticc/pb2/config.proto\x12\x16\x61rcticc.pb2.config_pb2\"\x95\x03\n\rRuntimeConfig\x12N\n\rstring_values\x18\x01 \x03(\x0b\x32\x37.arcticc.pb2.config_pb2.RuntimeConfig.StringValuesEntry\x12H\n\nint_values\x18\x02 \x03(\x0b\x32\x34.arcticc.pb2.config_pb2.RuntimeConfig.IntValuesEntry\x12N\n\rdouble_values\x18\x03 \x03(\x0b\x32\x37.arcticc.pb2.config_pb2.RuntimeConfig.DoubleValuesEntry\x1a\x33\n\x11StringValuesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x30\n\x0eIntValuesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x03:\x02\x38\x01\x1a\x33\n\x11\x44oubleValuesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\x62\x06proto3'
)




_RUNTIMECONFIG_STRINGVALUESENTRY = _descriptor.Descriptor(
  name='StringValuesEntry',
  full_name='arcticc.pb2.config_pb2.RuntimeConfig.StringValuesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='arcticc.pb2.config_pb2.RuntimeConfig.StringValuesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='arcticc.pb2.config_pb2.RuntimeConfig.StringValuesEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=304,
  serialized_end=355,
)

_RUNTIMECONFIG_INTVALUESENTRY = _descriptor.Descriptor(
  name='IntValuesEntry',
  full_name='arcticc.pb2.config_pb2.RuntimeConfig.IntValuesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='arcticc.pb2.config_pb2.RuntimeConfig.IntValuesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='arcticc.pb2.config_pb2.RuntimeConfig.IntValuesEntry.value', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=357,
  serialized_end=405,
)

_RUNTIMECONFIG_DOUBLEVALUESENTRY = _descriptor.Descriptor(
  name='DoubleValuesEntry',
  full_name='arcticc.pb2.config_pb2.RuntimeConfig.DoubleValuesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='arcticc.pb2.config_pb2.RuntimeConfig.DoubleValuesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='arcticc.pb2.config_pb2.RuntimeConfig.DoubleValuesEntry.value', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=407,
  serialized_end=458,
)

_RUNTIMECONFIG = _descriptor.Descriptor(
  name='RuntimeConfig',
  full_name='arcticc.pb2.config_pb2.RuntimeConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='string_values', full_name='arcticc.pb2.config_pb2.RuntimeConfig.string_values', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='int_values', full_name='arcticc.pb2.config_pb2.RuntimeConfig.int_values', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='double_values', full_name='arcticc.pb2.config_pb2.RuntimeConfig.double_values', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_RUNTIMECONFIG_STRINGVALUESENTRY, _RUNTIMECONFIG_INTVALUESENTRY, _RUNTIMECONFIG_DOUBLEVALUESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=53,
  serialized_end=458,
)

_RUNTIMECONFIG_STRINGVALUESENTRY.containing_type = _RUNTIMECONFIG
_RUNTIMECONFIG_INTVALUESENTRY.containing_type = _RUNTIMECONFIG
_RUNTIMECONFIG_DOUBLEVALUESENTRY.containing_type = _RUNTIMECONFIG
_RUNTIMECONFIG.fields_by_name['string_values'].message_type = _RUNTIMECONFIG_STRINGVALUESENTRY
_RUNTIMECONFIG.fields_by_name['int_values'].message_type = _RUNTIMECONFIG_INTVALUESENTRY
_RUNTIMECONFIG.fields_by_name['double_values'].message_type = _RUNTIMECONFIG_DOUBLEVALUESENTRY
DESCRIPTOR.message_types_by_name['RuntimeConfig'] = _RUNTIMECONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RuntimeConfig = _reflection.GeneratedProtocolMessageType('RuntimeConfig', (_message.Message,), {

  'StringValuesEntry' : _reflection.GeneratedProtocolMessageType('StringValuesEntry', (_message.Message,), {
    'DESCRIPTOR' : _RUNTIMECONFIG_STRINGVALUESENTRY,
    '__module__' : 'arcticc.pb2.config_pb2'
    # @@protoc_insertion_point(class_scope:arcticc.pb2.config_pb2.RuntimeConfig.StringValuesEntry)
    })
  ,

  'IntValuesEntry' : _reflection.GeneratedProtocolMessageType('IntValuesEntry', (_message.Message,), {
    'DESCRIPTOR' : _RUNTIMECONFIG_INTVALUESENTRY,
    '__module__' : 'arcticc.pb2.config_pb2'
    # @@protoc_insertion_point(class_scope:arcticc.pb2.config_pb2.RuntimeConfig.IntValuesEntry)
    })
  ,

  'DoubleValuesEntry' : _reflection.GeneratedProtocolMessageType('DoubleValuesEntry', (_message.Message,), {
    'DESCRIPTOR' : _RUNTIMECONFIG_DOUBLEVALUESENTRY,
    '__module__' : 'arcticc.pb2.config_pb2'
    # @@protoc_insertion_point(class_scope:arcticc.pb2.config_pb2.RuntimeConfig.DoubleValuesEntry)
    })
  ,
  'DESCRIPTOR' : _RUNTIMECONFIG,
  '__module__' : 'arcticc.pb2.config_pb2'
  # @@protoc_insertion_point(class_scope:arcticc.pb2.config_pb2.RuntimeConfig)
  })
_sym_db.RegisterMessage(RuntimeConfig)
_sym_db.RegisterMessage(RuntimeConfig.StringValuesEntry)
_sym_db.RegisterMessage(RuntimeConfig.IntValuesEntry)
_sym_db.RegisterMessage(RuntimeConfig.DoubleValuesEntry)


_RUNTIMECONFIG_STRINGVALUESENTRY._options = None
_RUNTIMECONFIG_INTVALUESENTRY._options = None
_RUNTIMECONFIG_DOUBLEVALUESENTRY._options = None
# @@protoc_insertion_point(module_scope)
