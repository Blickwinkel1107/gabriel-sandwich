# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: instruction.proto

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
  name='instruction.proto',
  package='instruction',
  syntax='proto3',
  serialized_pb=_b('\n\x11instruction.proto\x12\x0binstruction\"\xe9\x01\n\x08Sandwich\x12*\n\x05state\x18\x01 \x01(\x0e\x32\x1b.instruction.Sandwich.State\x12\x0e\n\x06holo_x\x18\x02 \x01(\x01\x12\x0e\n\x06holo_y\x18\x03 \x01(\x01\x12\x12\n\nholo_depth\x18\x04 \x01(\x01\"}\n\x05State\x12\t\n\x05START\x10\x00\x12\x0b\n\x07NOTHING\x10\x01\x12\t\n\x05\x42READ\x10\x02\x12\x07\n\x03HAM\x10\x03\x12\x0b\n\x07LETTUCE\x10\x04\x12\x0c\n\x08\x43UCUMBER\x10\x05\x12\x08\n\x04HALF\x10\x06\x12\n\n\x06TOMATO\x10\x07\x12\r\n\tHAM_WRONG\x10\x08\x12\x08\n\x04\x46ULL\x10\t\"X\n\x0c\x45ngineFields\x12\x14\n\x0cupdate_count\x18\x01 \x01(\x03\x12)\n\x08sandwich\x18\x03 \x01(\x0b\x32\x15.instruction.SandwichH\x00\x42\x07\n\x05stateB(\n\x1e\x65\x64u.cmu.cs.gabriel.instructionB\x06Protosb\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_SANDWICH_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='instruction.Sandwich.State',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='START', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NOTHING', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BREAD', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HAM', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LETTUCE', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CUCUMBER', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HALF', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOMATO', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HAM_WRONG', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FULL', index=9, number=9,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=143,
  serialized_end=268,
)
_sym_db.RegisterEnumDescriptor(_SANDWICH_STATE)


_SANDWICH = _descriptor.Descriptor(
  name='Sandwich',
  full_name='instruction.Sandwich',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='instruction.Sandwich.state', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='holo_x', full_name='instruction.Sandwich.holo_x', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='holo_y', full_name='instruction.Sandwich.holo_y', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='holo_depth', full_name='instruction.Sandwich.holo_depth', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SANDWICH_STATE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=35,
  serialized_end=268,
)


_ENGINEFIELDS = _descriptor.Descriptor(
  name='EngineFields',
  full_name='instruction.EngineFields',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='update_count', full_name='instruction.EngineFields.update_count', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sandwich', full_name='instruction.EngineFields.sandwich', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
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
      name='state', full_name='instruction.EngineFields.state',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=270,
  serialized_end=358,
)

_SANDWICH.fields_by_name['state'].enum_type = _SANDWICH_STATE
_SANDWICH_STATE.containing_type = _SANDWICH
_ENGINEFIELDS.fields_by_name['sandwich'].message_type = _SANDWICH
_ENGINEFIELDS.oneofs_by_name['state'].fields.append(
  _ENGINEFIELDS.fields_by_name['sandwich'])
_ENGINEFIELDS.fields_by_name['sandwich'].containing_oneof = _ENGINEFIELDS.oneofs_by_name['state']
DESCRIPTOR.message_types_by_name['Sandwich'] = _SANDWICH
DESCRIPTOR.message_types_by_name['EngineFields'] = _ENGINEFIELDS

Sandwich = _reflection.GeneratedProtocolMessageType('Sandwich', (_message.Message,), dict(
  DESCRIPTOR = _SANDWICH,
  __module__ = 'instruction_pb2'
  # @@protoc_insertion_point(class_scope:instruction.Sandwich)
  ))
_sym_db.RegisterMessage(Sandwich)

EngineFields = _reflection.GeneratedProtocolMessageType('EngineFields', (_message.Message,), dict(
  DESCRIPTOR = _ENGINEFIELDS,
  __module__ = 'instruction_pb2'
  # @@protoc_insertion_point(class_scope:instruction.EngineFields)
  ))
_sym_db.RegisterMessage(EngineFields)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\036edu.cmu.cs.gabriel.instructionB\006Protos'))
# @@protoc_insertion_point(module_scope)
