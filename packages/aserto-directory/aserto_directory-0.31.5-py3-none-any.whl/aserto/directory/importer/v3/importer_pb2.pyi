from aserto.directory.common.v3 import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Opcode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPCODE_UNKNOWN: _ClassVar[Opcode]
    OPCODE_SET: _ClassVar[Opcode]
    OPCODE_DELETE: _ClassVar[Opcode]
    OPCODE_DELETE_WITH_RELATIONS: _ClassVar[Opcode]
OPCODE_UNKNOWN: Opcode
OPCODE_SET: Opcode
OPCODE_DELETE: Opcode
OPCODE_DELETE_WITH_RELATIONS: Opcode

class ImportRequest(_message.Message):
    __slots__ = ("op_code", "object", "relation")
    OP_CODE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    RELATION_FIELD_NUMBER: _ClassVar[int]
    op_code: Opcode
    object: _common_pb2.Object
    relation: _common_pb2.Relation
    def __init__(self, op_code: _Optional[_Union[Opcode, str]] = ..., object: _Optional[_Union[_common_pb2.Object, _Mapping]] = ..., relation: _Optional[_Union[_common_pb2.Relation, _Mapping]] = ...) -> None: ...

class ImportResponse(_message.Message):
    __slots__ = ("object", "relation", "status", "counter")
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    RELATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COUNTER_FIELD_NUMBER: _ClassVar[int]
    object: ImportCounter
    relation: ImportCounter
    status: ImportStatus
    counter: ImportCounter
    def __init__(self, object: _Optional[_Union[ImportCounter, _Mapping]] = ..., relation: _Optional[_Union[ImportCounter, _Mapping]] = ..., status: _Optional[_Union[ImportStatus, _Mapping]] = ..., counter: _Optional[_Union[ImportCounter, _Mapping]] = ...) -> None: ...

class ImportCounter(_message.Message):
    __slots__ = ("recv", "set", "delete", "error", "type")
    RECV_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    DELETE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    recv: int
    set: int
    delete: int
    error: int
    type: str
    def __init__(self, recv: _Optional[int] = ..., set: _Optional[int] = ..., delete: _Optional[int] = ..., error: _Optional[int] = ..., type: _Optional[str] = ...) -> None: ...

class ImportStatus(_message.Message):
    __slots__ = ("code", "msg", "req")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    REQ_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    req: ImportRequest
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., req: _Optional[_Union[ImportRequest, _Mapping]] = ...) -> None: ...
