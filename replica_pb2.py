# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: replica.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='replica.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\rreplica.proto\"W\n\x06GetKey\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\x13\n\x0b\x66rom_client\x18\x02 \x01(\r\x12\x19\n\x11\x63onsistency_level\x18\x03 \x01(\t\x12\x10\n\x08\x66rom_rep\x18\x04 \x01(\t\"y\n\x06PutKey\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\t\x12\x13\n\x0b\x66rom_client\x18\x03 \x01(\r\x12\x11\n\ttimestamp\x18\x04 \x01(\t\x12\x19\n\x11\x63onsistency_level\x18\x05 \x01(\t\x12\x10\n\x08\x66rom_rep\x18\x06 \x01(\t\"A\n\x0c\x43ordResponse\x12\x15\n\rvalue_present\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\t\x12\x0b\n\x03\x61\x63k\x18\x03 \x01(\r\"p\n\x0fReplicaResponse\x12\x12\n\nis_updated\x18\x01 \x01(\r\x12\x15\n\rvalue_present\x18\x02 \x01(\r\x12\r\n\x05value\x18\x03 \x01(\t\x12\x11\n\ttimestamp\x18\x04 \x01(\t\x12\x10\n\x08\x66rom_rep\x18\x05 \x01(\t\"\xb1\x01\n\x0eReplicaMessage\x12\x1a\n\x07get_key\x18\x01 \x01(\x0b\x32\x07.GetKeyH\x00\x12\x1a\n\x07put_key\x18\x02 \x01(\x0b\x32\x07.PutKeyH\x00\x12&\n\rcord_response\x18\x03 \x01(\x0b\x32\r.CordResponseH\x00\x12,\n\x10replica_response\x18\x04 \x01(\x0b\x32\x10.ReplicaResponseH\x00\x42\x11\n\x0freplica_messageb\x06proto3')
)




_GETKEY = _descriptor.Descriptor(
  name='GetKey',
  full_name='GetKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='GetKey.key', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='from_client', full_name='GetKey.from_client', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='consistency_level', full_name='GetKey.consistency_level', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='from_rep', full_name='GetKey.from_rep', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=104,
)


_PUTKEY = _descriptor.Descriptor(
  name='PutKey',
  full_name='PutKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='PutKey.key', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='PutKey.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='from_client', full_name='PutKey.from_client', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='PutKey.timestamp', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='consistency_level', full_name='PutKey.consistency_level', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='from_rep', full_name='PutKey.from_rep', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=106,
  serialized_end=227,
)


_CORDRESPONSE = _descriptor.Descriptor(
  name='CordResponse',
  full_name='CordResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value_present', full_name='CordResponse.value_present', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='CordResponse.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ack', full_name='CordResponse.ack', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=229,
  serialized_end=294,
)


_REPLICARESPONSE = _descriptor.Descriptor(
  name='ReplicaResponse',
  full_name='ReplicaResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='is_updated', full_name='ReplicaResponse.is_updated', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value_present', full_name='ReplicaResponse.value_present', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='ReplicaResponse.value', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='ReplicaResponse.timestamp', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='from_rep', full_name='ReplicaResponse.from_rep', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=296,
  serialized_end=408,
)


_REPLICAMESSAGE = _descriptor.Descriptor(
  name='ReplicaMessage',
  full_name='ReplicaMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='get_key', full_name='ReplicaMessage.get_key', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='put_key', full_name='ReplicaMessage.put_key', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cord_response', full_name='ReplicaMessage.cord_response', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='replica_response', full_name='ReplicaMessage.replica_response', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='replica_message', full_name='ReplicaMessage.replica_message',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=411,
  serialized_end=588,
)

_REPLICAMESSAGE.fields_by_name['get_key'].message_type = _GETKEY
_REPLICAMESSAGE.fields_by_name['put_key'].message_type = _PUTKEY
_REPLICAMESSAGE.fields_by_name['cord_response'].message_type = _CORDRESPONSE
_REPLICAMESSAGE.fields_by_name['replica_response'].message_type = _REPLICARESPONSE
_REPLICAMESSAGE.oneofs_by_name['replica_message'].fields.append(
  _REPLICAMESSAGE.fields_by_name['get_key'])
_REPLICAMESSAGE.fields_by_name['get_key'].containing_oneof = _REPLICAMESSAGE.oneofs_by_name['replica_message']
_REPLICAMESSAGE.oneofs_by_name['replica_message'].fields.append(
  _REPLICAMESSAGE.fields_by_name['put_key'])
_REPLICAMESSAGE.fields_by_name['put_key'].containing_oneof = _REPLICAMESSAGE.oneofs_by_name['replica_message']
_REPLICAMESSAGE.oneofs_by_name['replica_message'].fields.append(
  _REPLICAMESSAGE.fields_by_name['cord_response'])
_REPLICAMESSAGE.fields_by_name['cord_response'].containing_oneof = _REPLICAMESSAGE.oneofs_by_name['replica_message']
_REPLICAMESSAGE.oneofs_by_name['replica_message'].fields.append(
  _REPLICAMESSAGE.fields_by_name['replica_response'])
_REPLICAMESSAGE.fields_by_name['replica_response'].containing_oneof = _REPLICAMESSAGE.oneofs_by_name['replica_message']
DESCRIPTOR.message_types_by_name['GetKey'] = _GETKEY
DESCRIPTOR.message_types_by_name['PutKey'] = _PUTKEY
DESCRIPTOR.message_types_by_name['CordResponse'] = _CORDRESPONSE
DESCRIPTOR.message_types_by_name['ReplicaResponse'] = _REPLICARESPONSE
DESCRIPTOR.message_types_by_name['ReplicaMessage'] = _REPLICAMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetKey = _reflection.GeneratedProtocolMessageType('GetKey', (_message.Message,), dict(
  DESCRIPTOR = _GETKEY,
  __module__ = 'replica_pb2'
  # @@protoc_insertion_point(class_scope:GetKey)
  ))
_sym_db.RegisterMessage(GetKey)

PutKey = _reflection.GeneratedProtocolMessageType('PutKey', (_message.Message,), dict(
  DESCRIPTOR = _PUTKEY,
  __module__ = 'replica_pb2'
  # @@protoc_insertion_point(class_scope:PutKey)
  ))
_sym_db.RegisterMessage(PutKey)

CordResponse = _reflection.GeneratedProtocolMessageType('CordResponse', (_message.Message,), dict(
  DESCRIPTOR = _CORDRESPONSE,
  __module__ = 'replica_pb2'
  # @@protoc_insertion_point(class_scope:CordResponse)
  ))
_sym_db.RegisterMessage(CordResponse)

ReplicaResponse = _reflection.GeneratedProtocolMessageType('ReplicaResponse', (_message.Message,), dict(
  DESCRIPTOR = _REPLICARESPONSE,
  __module__ = 'replica_pb2'
  # @@protoc_insertion_point(class_scope:ReplicaResponse)
  ))
_sym_db.RegisterMessage(ReplicaResponse)

ReplicaMessage = _reflection.GeneratedProtocolMessageType('ReplicaMessage', (_message.Message,), dict(
  DESCRIPTOR = _REPLICAMESSAGE,
  __module__ = 'replica_pb2'
  # @@protoc_insertion_point(class_scope:ReplicaMessage)
  ))
_sym_db.RegisterMessage(ReplicaMessage)


# @@protoc_insertion_point(module_scope)
