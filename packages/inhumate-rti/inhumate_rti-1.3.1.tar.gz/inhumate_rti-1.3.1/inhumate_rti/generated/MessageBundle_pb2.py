# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: MessageBundle.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MessageBundle.proto\x12\x12inhumate.rti.proto\"\xb2\x04\n\rMessageBundle\x12<\n\x07request\x18\x01 \x01(\x0b\x32).inhumate.rti.proto.MessageBundle.RequestH\x00\x12>\n\x08response\x18\x02 \x01(\x0b\x32*.inhumate.rti.proto.MessageBundle.ResponseH\x00\x1a\xbb\x01\n\x07Request\x12\x18\n\x10response_channel\x18\x01 \x01(\t\x12\x10\n\x08\x63hannels\x18\x02 \x03(\t\x12\x11\n\tfrom_time\x18\x03 \x01(\x01\x12\x0f\n\x07to_time\x18\x04 \x01(\x01\x12\r\n\x05limit\x18\x05 \x01(\x05\x12\x0e\n\x06offset\x18\x06 \x01(\x05\x12\x0f\n\x07reverse\x18\x07 \x01(\x08\x12\x13\n\x0bper_channel\x18\x08 \x01(\x08\x12\x0e\n\x06per_id\x18\t \x01(\x08\x12\x0b\n\x03ids\x18\n \x03(\t\x1a\\\n\x08Response\x12;\n\x08\x63hannels\x18\x01 \x03(\x0b\x32).inhumate.rti.proto.MessageBundle.Channel\x12\x13\n\x0btotal_count\x18\x02 \x01(\x03\x1aT\n\x07\x43hannel\x12\x0c\n\x04name\x18\x01 \x01(\t\x12;\n\x08messages\x18\x02 \x03(\x0b\x32).inhumate.rti.proto.MessageBundle.Message\x1a(\n\x07Message\x12\x0c\n\x04time\x18\x01 \x01(\x01\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\tB\x07\n\x05whichB\x15\xaa\x02\x12Inhumate.RTI.Protob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'MessageBundle_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\252\002\022Inhumate.RTI.Proto'
  _globals['_MESSAGEBUNDLE']._serialized_start=44
  _globals['_MESSAGEBUNDLE']._serialized_end=606
  _globals['_MESSAGEBUNDLE_REQUEST']._serialized_start=188
  _globals['_MESSAGEBUNDLE_REQUEST']._serialized_end=375
  _globals['_MESSAGEBUNDLE_RESPONSE']._serialized_start=377
  _globals['_MESSAGEBUNDLE_RESPONSE']._serialized_end=469
  _globals['_MESSAGEBUNDLE_CHANNEL']._serialized_start=471
  _globals['_MESSAGEBUNDLE_CHANNEL']._serialized_end=555
  _globals['_MESSAGEBUNDLE_MESSAGE']._serialized_start=557
  _globals['_MESSAGEBUNDLE_MESSAGE']._serialized_end=597
# @@protoc_insertion_point(module_scope)
