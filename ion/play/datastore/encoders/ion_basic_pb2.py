# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


DESCRIPTOR = descriptor.FileDescriptor(
  name='ion_basic.proto',
  package='ion',
  serialized_pb='\n\x0fion_basic.proto\x12\x03ion\"\x18\n\x07\x46loat32\x12\r\n\x05value\x18\x01 \x02(\x02\"\x18\n\x07\x46loat64\x12\r\n\x05value\x18\x01 \x02(\x01\"\x16\n\x05Int32\x12\r\n\x05value\x18\x01 \x02(\x05\"\x16\n\x05Int64\x12\r\n\x05value\x18\x01 \x02(\x03\"\x17\n\x06UInt32\x12\r\n\x05value\x18\x01 \x02(\r\"\x17\n\x06UInt64\x12\r\n\x05value\x18\x01 \x02(\x04\"\x17\n\x06String\x12\r\n\x05value\x18\x01 \x02(\t\"\x18\n\x07\x42oolean\x12\r\n\x05value\x18\x01 \x02(\x08\"\x15\n\x04\x42yte\x12\r\n\x05value\x18\x01 \x02(\x0c\"\x16\n\x05\x42ytes\x12\r\n\x05value\x18\x01 \x02(\x0c\"+\n\rCompositeType\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0c\n\x04type\x18\x02 \x02(\x05\"y\n\tStructure\x12.\n\x05items\x18\x01 \x03(\x0b\x32\x1f.ion.Structure.StructureElement\x1a<\n\x10StructureElement\x12\x0b\n\x03key\x18\x01 \x02(\t\x12\x0c\n\x04type\x18\x02 \x02(\t\x12\r\n\x05value\x18\x03 \x02(\x0c\")\n\nTypedValue\x12\x0c\n\x04type\x18\x01 \x02(\t\x12\r\n\x05value\x18\x02 \x02(\x0c\"^\n\nDataObject\x12\'\n\x04\x61tts\x18\x01 \x03(\x0b\x32\x19.ion.DataObject.Attribute\x1a\'\n\tAttribute\x12\x0b\n\x03key\x18\x01 \x02(\t\x12\r\n\x05value\x18\x02 \x02(\x0c\"\x82\x01\n\x15\x44\x61taObjectDescription\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x32\n\x04\x61tts\x18\x02 \x03(\x0b\x32$.ion.DataObjectDescription.Attribute\x1a\'\n\tAttribute\x12\x0b\n\x03key\x18\x01 \x02(\t\x12\r\n\x05value\x18\x02 \x02(\x0c\"I\n\x0e\x44\x61taObjectNode\x12\n\n\x02id\x18\x01 \x02(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x02(\x0c\x12\x0c\n\x04type\x18\x03 \x02(\x0c\x12\x0c\n\x04\x66lag\x18\x04 \x02(\x0c\"\x1a\n\tContainer\x12\r\n\x05items\x18\x01 \x03(\x0c\"O\n\x07\x43\x41Store\x12 \n\x05nodes\x18\x01 \x03(\x0b\x32\x11.ion.CAStore.Node\x1a\"\n\x04Node\x12\x0b\n\x03key\x18\x01 \x02(\x0c\x12\r\n\x05value\x18\x02 \x02(\x0c\x42\x14\n\x08ion.dataB\x08IONTypes')




_FLOAT32 = descriptor.Descriptor(
  name='Float32',
  full_name='ion.Float32',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='value', full_name='ion.Float32.value', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  serialized_start=24,
  serialized_end=48,
)


_FLOAT64 = descriptor.Descriptor(
  name='Float64',
  full_name='ion.Float64',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='value', full_name='ion.Float64.value', index=0,
      number=1, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  serialized_start=50,
  serialized_end=74,
)


_INT32 = descriptor.Descriptor(
  name='Int32',
  full_name='ion.Int32',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='value', full_name='ion.Int32.value', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  serialized_start=76,
  serialized_end=98,
)


_INT64 = descriptor.Descriptor(
  name='Int64',
  full_name='ion.Int64',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='value', full_name='ion.Int64.value', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  serialized_start=100,
  serialized_end=122,
)


_UINT32 = descriptor.Descriptor(
  name='UInt32',
  full_name='ion.UInt32',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='value', full_name='ion.UInt32.value', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  serialized_start=124,
  serialized_end=147,
)


_UINT64 = descriptor.Descriptor(
  name='UInt64',
  full_name='ion.UInt64',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='value', full_name='ion.UInt64.value', index=0,
      number=1, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  serialized_start=149,
  serialized_end=172,
)


_STRING = descriptor.Descriptor(
  name='String',
  full_name='ion.String',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='value', full_name='ion.String.value', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  extension_ranges=[],
  serialized_start=174,
  serialized_end=197,
)


_BOOLEAN = descriptor.Descriptor(
  name='Boolean',
  full_name='ion.Boolean',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='value', full_name='ion.Boolean.value', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
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
  extension_ranges=[],
  serialized_start=199,
  serialized_end=223,
)


_BYTE = descriptor.Descriptor(
  name='Byte',
  full_name='ion.Byte',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='value', full_name='ion.Byte.value', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
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
  extension_ranges=[],
  serialized_start=225,
  serialized_end=246,
)


_BYTES = descriptor.Descriptor(
  name='Bytes',
  full_name='ion.Bytes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='value', full_name='ion.Bytes.value', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
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
  extension_ranges=[],
  serialized_start=248,
  serialized_end=270,
)


_COMPOSITETYPE = descriptor.Descriptor(
  name='CompositeType',
  full_name='ion.CompositeType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='name', full_name='ion.CompositeType.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='type', full_name='ion.CompositeType.type', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  serialized_start=272,
  serialized_end=315,
)


_STRUCTURE_STRUCTUREELEMENT = descriptor.Descriptor(
  name='StructureElement',
  full_name='ion.Structure.StructureElement',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='key', full_name='ion.Structure.StructureElement.key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='type', full_name='ion.Structure.StructureElement.type', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='value', full_name='ion.Structure.StructureElement.value', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
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
  extension_ranges=[],
  serialized_start=378,
  serialized_end=438,
)

_STRUCTURE = descriptor.Descriptor(
  name='Structure',
  full_name='ion.Structure',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='items', full_name='ion.Structure.items', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_STRUCTURE_STRUCTUREELEMENT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=317,
  serialized_end=438,
)


_TYPEDVALUE = descriptor.Descriptor(
  name='TypedValue',
  full_name='ion.TypedValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='type', full_name='ion.TypedValue.type', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='value', full_name='ion.TypedValue.value', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
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
  extension_ranges=[],
  serialized_start=440,
  serialized_end=481,
)


_DATAOBJECT_ATTRIBUTE = descriptor.Descriptor(
  name='Attribute',
  full_name='ion.DataObject.Attribute',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='key', full_name='ion.DataObject.Attribute.key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='value', full_name='ion.DataObject.Attribute.value', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
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
  extension_ranges=[],
  serialized_start=538,
  serialized_end=577,
)

_DATAOBJECT = descriptor.Descriptor(
  name='DataObject',
  full_name='ion.DataObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='atts', full_name='ion.DataObject.atts', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DATAOBJECT_ATTRIBUTE, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=483,
  serialized_end=577,
)


_DATAOBJECTDESCRIPTION_ATTRIBUTE = descriptor.Descriptor(
  name='Attribute',
  full_name='ion.DataObjectDescription.Attribute',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='key', full_name='ion.DataObjectDescription.Attribute.key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='value', full_name='ion.DataObjectDescription.Attribute.value', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
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
  extension_ranges=[],
  serialized_start=538,
  serialized_end=577,
)

_DATAOBJECTDESCRIPTION = descriptor.Descriptor(
  name='DataObjectDescription',
  full_name='ion.DataObjectDescription',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='name', full_name='ion.DataObjectDescription.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='atts', full_name='ion.DataObjectDescription.atts', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DATAOBJECTDESCRIPTION_ATTRIBUTE, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=580,
  serialized_end=710,
)


_DATAOBJECTNODE = descriptor.Descriptor(
  name='DataObjectNode',
  full_name='ion.DataObjectNode',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='ion.DataObjectNode.id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='content', full_name='ion.DataObjectNode.content', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='type', full_name='ion.DataObjectNode.type', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='flag', full_name='ion.DataObjectNode.flag', index=3,
      number=4, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
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
  extension_ranges=[],
  serialized_start=712,
  serialized_end=785,
)


_CONTAINER = descriptor.Descriptor(
  name='Container',
  full_name='ion.Container',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='items', full_name='ion.Container.items', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  extension_ranges=[],
  serialized_start=787,
  serialized_end=813,
)


_CASTORE_NODE = descriptor.Descriptor(
  name='Node',
  full_name='ion.CAStore.Node',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='key', full_name='ion.CAStore.Node.key', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='value', full_name='ion.CAStore.Node.value', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
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
  extension_ranges=[],
  serialized_start=860,
  serialized_end=894,
)

_CASTORE = descriptor.Descriptor(
  name='CAStore',
  full_name='ion.CAStore',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='nodes', full_name='ion.CAStore.nodes', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_CASTORE_NODE, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=815,
  serialized_end=894,
)


_STRUCTURE_STRUCTUREELEMENT.containing_type = _STRUCTURE;
_STRUCTURE.fields_by_name['items'].message_type = _STRUCTURE_STRUCTUREELEMENT
_DATAOBJECT_ATTRIBUTE.containing_type = _DATAOBJECT;
_DATAOBJECT.fields_by_name['atts'].message_type = _DATAOBJECT_ATTRIBUTE
_DATAOBJECTDESCRIPTION_ATTRIBUTE.containing_type = _DATAOBJECTDESCRIPTION;
_DATAOBJECTDESCRIPTION.fields_by_name['atts'].message_type = _DATAOBJECTDESCRIPTION_ATTRIBUTE
_CASTORE_NODE.containing_type = _CASTORE;
_CASTORE.fields_by_name['nodes'].message_type = _CASTORE_NODE

class Float32(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FLOAT32
  
  # @@protoc_insertion_point(class_scope:ion.Float32)

class Float64(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FLOAT64
  
  # @@protoc_insertion_point(class_scope:ion.Float64)

class Int32(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INT32
  
  # @@protoc_insertion_point(class_scope:ion.Int32)

class Int64(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INT64
  
  # @@protoc_insertion_point(class_scope:ion.Int64)

class UInt32(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _UINT32
  
  # @@protoc_insertion_point(class_scope:ion.UInt32)

class UInt64(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _UINT64
  
  # @@protoc_insertion_point(class_scope:ion.UInt64)

class String(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _STRING
  
  # @@protoc_insertion_point(class_scope:ion.String)

class Boolean(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BOOLEAN
  
  # @@protoc_insertion_point(class_scope:ion.Boolean)

class Byte(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BYTE
  
  # @@protoc_insertion_point(class_scope:ion.Byte)

class Bytes(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BYTES
  
  # @@protoc_insertion_point(class_scope:ion.Bytes)

class CompositeType(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _COMPOSITETYPE
  
  # @@protoc_insertion_point(class_scope:ion.CompositeType)

class Structure(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class StructureElement(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STRUCTURE_STRUCTUREELEMENT
    
    # @@protoc_insertion_point(class_scope:ion.Structure.StructureElement)
  DESCRIPTOR = _STRUCTURE
  
  # @@protoc_insertion_point(class_scope:ion.Structure)

class TypedValue(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TYPEDVALUE
  
  # @@protoc_insertion_point(class_scope:ion.TypedValue)

class DataObject(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Attribute(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _DATAOBJECT_ATTRIBUTE
    
    # @@protoc_insertion_point(class_scope:ion.DataObject.Attribute)
  DESCRIPTOR = _DATAOBJECT
  
  # @@protoc_insertion_point(class_scope:ion.DataObject)

class DataObjectDescription(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Attribute(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _DATAOBJECTDESCRIPTION_ATTRIBUTE
    
    # @@protoc_insertion_point(class_scope:ion.DataObjectDescription.Attribute)
  DESCRIPTOR = _DATAOBJECTDESCRIPTION
  
  # @@protoc_insertion_point(class_scope:ion.DataObjectDescription)

class DataObjectNode(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DATAOBJECTNODE
  
  # @@protoc_insertion_point(class_scope:ion.DataObjectNode)

class Container(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CONTAINER
  
  # @@protoc_insertion_point(class_scope:ion.Container)

class CAStore(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Node(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _CASTORE_NODE
    
    # @@protoc_insertion_point(class_scope:ion.CAStore.Node)
  DESCRIPTOR = _CASTORE
  
  # @@protoc_insertion_point(class_scope:ion.CAStore)

# @@protoc_insertion_point(module_scope)