# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: arcticc/pb2/encoding.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from arcticc.pb2 import descriptors_pb2 as arcticc_dot_pb2_dot_descriptors__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1a\x61rcticc/pb2/encoding.proto\x12\x18\x61rcticc.pb2.encoding_pb2\x1a\x1d\x61rcticc/pb2/descriptors.proto\"\x96\x03\n\rSegmentHeader\x12\x10\n\x08start_ts\x18\x01 \x01(\x04\x12\x0e\n\x06\x65nd_ts\x18\x02 \x01(\x04\x12H\n\x11stream_descriptor\x18\x03 \x01(\x0b\x32-.arcticc.pb2.descriptors_pb2.StreamDescriptor\x12\x36\n\x06\x66ields\x18\x05 \x03(\x0b\x32&.arcticc.pb2.encoding_pb2.EncodedField\x12>\n\x0emetadata_field\x18\x07 \x01(\x0b\x32&.arcticc.pb2.encoding_pb2.EncodedField\x12\x41\n\x11string_pool_field\x18\x08 \x01(\x0b\x32&.arcticc.pb2.encoding_pb2.EncodedField\x12\x11\n\tcompacted\x18\t \x01(\x08\x12\x18\n\x10\x65ncoding_version\x18\r \x01(\r\"%\n\x08HashType\x12\x0c\n\x08ROWCOUNT\x10\x00\x12\x0b\n\x07XX_HASH\x10\x01J\x04\x08\x06\x10\x07J\x04\x08\n\x10\r\"\xea\x01\n\nFieldStats\x12\x0b\n\x03min\x18\x01 \x01(\x04\x12\x0b\n\x03max\x18\x02 \x01(\x04\x12\x14\n\x0cunique_count\x18\x03 \x01(\r\x12\x0e\n\x06sorted\x18\x04 \x01(\x08\x12\x0b\n\x03set\x18\x05 \x01(\r\x12Y\n\x16unique_count_precision\x18\x06 \x01(\x0e\x32\x39.arcticc.pb2.encoding_pb2.FieldStats.UniqueCountPrecision\"4\n\x14UniqueCountPrecision\x12\x0b\n\x07PRECISE\x10\x00\x12\x0f\n\x0bHYPERLOGLOG\x10\x01\"\xff\x01\n\x0c\x45ncodedField\x12@\n\x07ndarray\x18\x02 \x01(\x0b\x32-.arcticc.pb2.encoding_pb2.NDArrayEncodedFieldH\x00\x12\x46\n\ndictionary\x18\x03 \x01(\x0b\x32\x30.arcticc.pb2.encoding_pb2.DictionaryEncodedFieldH\x00\x12\x0e\n\x06offset\x18\x04 \x01(\r\x12\x14\n\x0cnum_elements\x18\x05 \x01(\r\x12\x33\n\x05stats\x18\x06 \x01(\x0b\x32$.arcticc.pb2.encoding_pb2.FieldStatsB\n\n\x08\x65ncoding\"\xfd\x04\n\x0cVariantCodec\x12;\n\x04zstd\x18\x10 \x01(\x0b\x32+.arcticc.pb2.encoding_pb2.VariantCodec.ZstdH\x00\x12?\n\x03tp4\x18\x11 \x01(\x0b\x32\x30.arcticc.pb2.encoding_pb2.VariantCodec.TurboPforH\x00\x12\x39\n\x03lz4\x18\x12 \x01(\x0b\x32*.arcticc.pb2.encoding_pb2.VariantCodec.Lz4H\x00\x12I\n\x0bpassthrough\x18\x13 \x01(\x0b\x32\x32.arcticc.pb2.encoding_pb2.VariantCodec.PassthroughH\x00\x1a+\n\x04Zstd\x12\r\n\x05level\x18\x01 \x01(\x05\x12\x14\n\x0cis_streaming\x18\x02 \x01(\x08\x1a\xf8\x01\n\tTurboPfor\x12M\n\tsub_codec\x18\x01 \x01(\x0e\x32:.arcticc.pb2.encoding_pb2.VariantCodec.TurboPfor.SubCodecs\"\x9b\x01\n\tSubCodecs\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x06\n\x02P4\x10\x10\x12\x0c\n\x08P4_DELTA\x10\x11\x12\x10\n\x0cP4_DELTA_RLE\x10\x12\x12\t\n\x05P4_ZZ\x10\x14\x12\x0c\n\x08\x46P_DELTA\x10 \x12\x10\n\x0c\x46P_DELTA2_ZZ\x10!\x12\x12\n\x0e\x46P_GORILLA_RLE\x10\"\x12\t\n\x05\x46P_ZZ\x10$\x12\x0f\n\x0b\x46P_ZZ_DELTA\x10(\x1a\x1b\n\x03Lz4\x12\x14\n\x0c\x61\x63\x63\x65leration\x18\x01 \x01(\x05\x1a\x1b\n\x0bPassthrough\x12\x0c\n\x04mark\x18\x01 \x01(\x08\x42\x07\n\x05\x63odec\"\x8a\x01\n\x05\x42lock\x12\x10\n\x08in_bytes\x18\x01 \x01(\r\x12\x11\n\tout_bytes\x18\x02 \x01(\r\x12\x0c\n\x04hash\x18\x03 \x01(\x04\x12\x17\n\x0f\x65ncoder_version\x18\x04 \x01(\r\x12\x35\n\x05\x63odec\x18\x05 \x01(\x0b\x32&.arcticc.pb2.encoding_pb2.VariantCodec\"\xa6\x01\n\x13NDArrayEncodedField\x12\x13\n\x0bitems_count\x18\x01 \x01(\r\x12/\n\x06shapes\x18\x02 \x03(\x0b\x32\x1f.arcticc.pb2.encoding_pb2.Block\x12/\n\x06values\x18\x03 \x03(\x0b\x32\x1f.arcticc.pb2.encoding_pb2.Block\x12\x18\n\x10sparse_map_bytes\x18\x04 \x01(\r\"\x99\x01\n\x16\x44ictionaryEncodedField\x12=\n\x06values\x18\x01 \x01(\x0b\x32-.arcticc.pb2.encoding_pb2.NDArrayEncodedField\x12@\n\tpositions\x18\x02 \x01(\x0b\x32-.arcticc.pb2.encoding_pb2.NDArrayEncodedFieldB\x03\xf8\x01\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'arcticc.pb2.encoding_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\370\001\001'
  _globals['_SEGMENTHEADER']._serialized_start=88
  _globals['_SEGMENTHEADER']._serialized_end=494
  _globals['_SEGMENTHEADER_HASHTYPE']._serialized_start=445
  _globals['_SEGMENTHEADER_HASHTYPE']._serialized_end=482
  _globals['_FIELDSTATS']._serialized_start=497
  _globals['_FIELDSTATS']._serialized_end=731
  _globals['_FIELDSTATS_UNIQUECOUNTPRECISION']._serialized_start=679
  _globals['_FIELDSTATS_UNIQUECOUNTPRECISION']._serialized_end=731
  _globals['_ENCODEDFIELD']._serialized_start=734
  _globals['_ENCODEDFIELD']._serialized_end=989
  _globals['_VARIANTCODEC']._serialized_start=992
  _globals['_VARIANTCODEC']._serialized_end=1629
  _globals['_VARIANTCODEC_ZSTD']._serialized_start=1268
  _globals['_VARIANTCODEC_ZSTD']._serialized_end=1311
  _globals['_VARIANTCODEC_TURBOPFOR']._serialized_start=1314
  _globals['_VARIANTCODEC_TURBOPFOR']._serialized_end=1562
  _globals['_VARIANTCODEC_TURBOPFOR_SUBCODECS']._serialized_start=1407
  _globals['_VARIANTCODEC_TURBOPFOR_SUBCODECS']._serialized_end=1562
  _globals['_VARIANTCODEC_LZ4']._serialized_start=1564
  _globals['_VARIANTCODEC_LZ4']._serialized_end=1591
  _globals['_VARIANTCODEC_PASSTHROUGH']._serialized_start=1593
  _globals['_VARIANTCODEC_PASSTHROUGH']._serialized_end=1620
  _globals['_BLOCK']._serialized_start=1632
  _globals['_BLOCK']._serialized_end=1770
  _globals['_NDARRAYENCODEDFIELD']._serialized_start=1773
  _globals['_NDARRAYENCODEDFIELD']._serialized_end=1939
  _globals['_DICTIONARYENCODEDFIELD']._serialized_start=1942
  _globals['_DICTIONARYENCODEDFIELD']._serialized_end=2095
# @@protoc_insertion_point(module_scope)
