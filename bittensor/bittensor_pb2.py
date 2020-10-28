# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bittensor/bittensor.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='bittensor/bittensor.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x19\x62ittensor/bittensor.proto\"I\n\x0bGossipBatch\x12\x0f\n\x07version\x18\x01 \x01(\x02\x12\r\n\x05peers\x18\x02 \x03(\t\x12\x1a\n\x08synapses\x18\x03 \x03(\x0b\x32\x08.Synapse\"\xb0\x01\n\x07Synapse\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x12\n\nneuron_key\x18\x02 \x01(\t\x12\x13\n\x0bsynapse_key\x18\x03 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x04 \x01(\t\x12\x0c\n\x04port\x18\x05 \x01(\x05\x12\x12\n\nblock_hash\x18\x08 \x01(\t\x12\x0e\n\x06nounce\x18\t \x01(\x05\x12\x15\n\rproof_of_work\x18\n \x01(\x0c\x12\x11\n\tsignature\x18\x0b \x01(\x0c\"\x86\x01\n\rTensorMessage\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x12\n\nneuron_key\x18\x02 \x01(\t\x12\x13\n\x0bsynapse_key\x18\x03 \x01(\t\x12\x0e\n\x06nounce\x18\x04 \x01(\x03\x12\x11\n\tsignature\x18\x05 \x01(\x0c\x12\x18\n\x07tensors\x18\x06 \x03(\x0b\x32\x07.Tensor\"\x86\x01\n\x06Tensor\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x0e\n\x06\x62uffer\x18\x02 \x01(\x0c\x12\r\n\x05shape\x18\x03 \x03(\x03\x12\x18\n\x05\x64type\x18\x04 \x01(\x0e\x32\t.DataType\x12\x1b\n\x08modality\x18\x05 \x01(\x0e\x32\t.Modality\x12\x15\n\rrequires_grad\x18\x06 \x01(\x08*Q\n\x08\x44\x61taType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0b\n\x07\x46LOAT32\x10\x01\x12\x0b\n\x07\x46LOAT64\x10\x02\x12\t\n\x05INT32\x10\x03\x12\t\n\x05INT64\x10\x04\x12\x08\n\x04UTF8\x10\x05*+\n\x08Modality\x12\n\n\x06TENSOR\x10\x00\x12\t\n\x05IMAGE\x10\x01\x12\x08\n\x04TEXT\x10\x02\x32\x66\n\tBittensor\x12+\n\x07\x46orward\x12\x0e.TensorMessage\x1a\x0e.TensorMessage\"\x00\x12,\n\x08\x42\x61\x63kward\x12\x0e.TensorMessage\x1a\x0e.TensorMessage\"\x00\x32\x33\n\tMetagraph\x12&\n\x06Gossip\x12\x0c.GossipBatch\x1a\x0c.GossipBatch\"\x00\x62\x06proto3'
)

_DATATYPE = _descriptor.EnumDescriptor(
  name='DataType',
  full_name='DataType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FLOAT32', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FLOAT64', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INT32', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INT64', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UTF8', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=557,
  serialized_end=638,
)
_sym_db.RegisterEnumDescriptor(_DATATYPE)

DataType = enum_type_wrapper.EnumTypeWrapper(_DATATYPE)
_MODALITY = _descriptor.EnumDescriptor(
  name='Modality',
  full_name='Modality',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TENSOR', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='IMAGE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TEXT', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=640,
  serialized_end=683,
)
_sym_db.RegisterEnumDescriptor(_MODALITY)

Modality = enum_type_wrapper.EnumTypeWrapper(_MODALITY)
UNKNOWN = 0
FLOAT32 = 1
FLOAT64 = 2
INT32 = 3
INT64 = 4
UTF8 = 5
TENSOR = 0
IMAGE = 1
TEXT = 2



_GOSSIPBATCH = _descriptor.Descriptor(
  name='GossipBatch',
  full_name='GossipBatch',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='GossipBatch.version', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='peers', full_name='GossipBatch.peers', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='synapses', full_name='GossipBatch.synapses', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  ],
  serialized_start=29,
  serialized_end=102,
)


_SYNAPSE = _descriptor.Descriptor(
  name='Synapse',
  full_name='Synapse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='Synapse.version', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='neuron_key', full_name='Synapse.neuron_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='synapse_key', full_name='Synapse.synapse_key', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='address', full_name='Synapse.address', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='Synapse.port', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='block_hash', full_name='Synapse.block_hash', index=5,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nounce', full_name='Synapse.nounce', index=6,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='proof_of_work', full_name='Synapse.proof_of_work', index=7,
      number=10, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='signature', full_name='Synapse.signature', index=8,
      number=11, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  ],
  serialized_start=105,
  serialized_end=281,
)


_TENSORMESSAGE = _descriptor.Descriptor(
  name='TensorMessage',
  full_name='TensorMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='TensorMessage.version', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='neuron_key', full_name='TensorMessage.neuron_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='synapse_key', full_name='TensorMessage.synapse_key', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nounce', full_name='TensorMessage.nounce', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='signature', full_name='TensorMessage.signature', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tensors', full_name='TensorMessage.tensors', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  ],
  serialized_start=284,
  serialized_end=418,
)


_TENSOR = _descriptor.Descriptor(
  name='Tensor',
  full_name='Tensor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='Tensor.version', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='buffer', full_name='Tensor.buffer', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='shape', full_name='Tensor.shape', index=2,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dtype', full_name='Tensor.dtype', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='modality', full_name='Tensor.modality', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='requires_grad', full_name='Tensor.requires_grad', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  ],
  serialized_start=421,
  serialized_end=555,
)

_GOSSIPBATCH.fields_by_name['synapses'].message_type = _SYNAPSE
_TENSORMESSAGE.fields_by_name['tensors'].message_type = _TENSOR
_TENSOR.fields_by_name['dtype'].enum_type = _DATATYPE
_TENSOR.fields_by_name['modality'].enum_type = _MODALITY
DESCRIPTOR.message_types_by_name['GossipBatch'] = _GOSSIPBATCH
DESCRIPTOR.message_types_by_name['Synapse'] = _SYNAPSE
DESCRIPTOR.message_types_by_name['TensorMessage'] = _TENSORMESSAGE
DESCRIPTOR.message_types_by_name['Tensor'] = _TENSOR
DESCRIPTOR.enum_types_by_name['DataType'] = _DATATYPE
DESCRIPTOR.enum_types_by_name['Modality'] = _MODALITY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GossipBatch = _reflection.GeneratedProtocolMessageType('GossipBatch', (_message.Message,), {
  'DESCRIPTOR' : _GOSSIPBATCH,
  '__module__' : 'bittensor.bittensor_pb2'
  # @@protoc_insertion_point(class_scope:GossipBatch)
  })
_sym_db.RegisterMessage(GossipBatch)

Synapse = _reflection.GeneratedProtocolMessageType('Synapse', (_message.Message,), {
  'DESCRIPTOR' : _SYNAPSE,
  '__module__' : 'bittensor.bittensor_pb2'
  # @@protoc_insertion_point(class_scope:Synapse)
  })
_sym_db.RegisterMessage(Synapse)

TensorMessage = _reflection.GeneratedProtocolMessageType('TensorMessage', (_message.Message,), {
  'DESCRIPTOR' : _TENSORMESSAGE,
  '__module__' : 'bittensor.bittensor_pb2'
  # @@protoc_insertion_point(class_scope:TensorMessage)
  })
_sym_db.RegisterMessage(TensorMessage)

Tensor = _reflection.GeneratedProtocolMessageType('Tensor', (_message.Message,), {
  'DESCRIPTOR' : _TENSOR,
  '__module__' : 'bittensor.bittensor_pb2'
  # @@protoc_insertion_point(class_scope:Tensor)
  })
_sym_db.RegisterMessage(Tensor)



_BITTENSOR = _descriptor.ServiceDescriptor(
  name='Bittensor',
  full_name='Bittensor',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=685,
  serialized_end=787,
  methods=[
  _descriptor.MethodDescriptor(
    name='Forward',
    full_name='Bittensor.Forward',
    index=0,
    containing_service=None,
    input_type=_TENSORMESSAGE,
    output_type=_TENSORMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Backward',
    full_name='Bittensor.Backward',
    index=1,
    containing_service=None,
    input_type=_TENSORMESSAGE,
    output_type=_TENSORMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_BITTENSOR)

DESCRIPTOR.services_by_name['Bittensor'] = _BITTENSOR


_METAGRAPH = _descriptor.ServiceDescriptor(
  name='Metagraph',
  full_name='Metagraph',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=789,
  serialized_end=840,
  methods=[
  _descriptor.MethodDescriptor(
    name='Gossip',
    full_name='Metagraph.Gossip',
    index=0,
    containing_service=None,
    input_type=_GOSSIPBATCH,
    output_type=_GOSSIPBATCH,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_METAGRAPH)

DESCRIPTOR.services_by_name['Metagraph'] = _METAGRAPH

# @@protoc_insertion_point(module_scope)
