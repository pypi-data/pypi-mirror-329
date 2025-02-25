from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberNonlinearityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_NONLINEARITY_TYPE_FAILURE_IF_TENSION: _ClassVar[MemberNonlinearityType]
    MEMBER_NONLINEARITY_TYPE_FAILURE: _ClassVar[MemberNonlinearityType]
    MEMBER_NONLINEARITY_TYPE_FAILURE_IF_COMPRESSION: _ClassVar[MemberNonlinearityType]
    MEMBER_NONLINEARITY_TYPE_FAILURE_IF_COMPRESSION_WITH_SLIPPAGE: _ClassVar[MemberNonlinearityType]
    MEMBER_NONLINEARITY_TYPE_FAILURE_IF_TENSION_WITH_SLIPPAGE: _ClassVar[MemberNonlinearityType]
    MEMBER_NONLINEARITY_TYPE_FAILURE_UNDER_COMPRESSION: _ClassVar[MemberNonlinearityType]
    MEMBER_NONLINEARITY_TYPE_FAILURE_UNDER_TENSION: _ClassVar[MemberNonlinearityType]
    MEMBER_NONLINEARITY_TYPE_SLIPPAGE: _ClassVar[MemberNonlinearityType]
    MEMBER_NONLINEARITY_TYPE_YIELDING: _ClassVar[MemberNonlinearityType]
    MEMBER_NONLINEARITY_TYPE_YIELDING_UNDER_COMPRESSION: _ClassVar[MemberNonlinearityType]
    MEMBER_NONLINEARITY_TYPE_YIELDING_UNDER_TENSION: _ClassVar[MemberNonlinearityType]
MEMBER_NONLINEARITY_TYPE_FAILURE_IF_TENSION: MemberNonlinearityType
MEMBER_NONLINEARITY_TYPE_FAILURE: MemberNonlinearityType
MEMBER_NONLINEARITY_TYPE_FAILURE_IF_COMPRESSION: MemberNonlinearityType
MEMBER_NONLINEARITY_TYPE_FAILURE_IF_COMPRESSION_WITH_SLIPPAGE: MemberNonlinearityType
MEMBER_NONLINEARITY_TYPE_FAILURE_IF_TENSION_WITH_SLIPPAGE: MemberNonlinearityType
MEMBER_NONLINEARITY_TYPE_FAILURE_UNDER_COMPRESSION: MemberNonlinearityType
MEMBER_NONLINEARITY_TYPE_FAILURE_UNDER_TENSION: MemberNonlinearityType
MEMBER_NONLINEARITY_TYPE_SLIPPAGE: MemberNonlinearityType
MEMBER_NONLINEARITY_TYPE_YIELDING: MemberNonlinearityType
MEMBER_NONLINEARITY_TYPE_YIELDING_UNDER_COMPRESSION: MemberNonlinearityType
MEMBER_NONLINEARITY_TYPE_YIELDING_UNDER_TENSION: MemberNonlinearityType

class MemberNonlinearity(_message.Message):
    __slots__ = ("no", "type", "assigned_to", "comment", "compression_force", "generating_object_info", "is_generated", "name", "slippage", "tension_force", "user_defined_name_enabled", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_FORCE_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    TENSION_FORCE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: MemberNonlinearityType
    assigned_to: _containers.RepeatedScalarFieldContainer[int]
    comment: str
    compression_force: float
    generating_object_info: str
    is_generated: bool
    name: str
    slippage: float
    tension_force: float
    user_defined_name_enabled: bool
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[MemberNonlinearityType, str]] = ..., assigned_to: _Optional[_Iterable[int]] = ..., comment: _Optional[str] = ..., compression_force: _Optional[float] = ..., generating_object_info: _Optional[str] = ..., is_generated: bool = ..., name: _Optional[str] = ..., slippage: _Optional[float] = ..., tension_force: _Optional[float] = ..., user_defined_name_enabled: bool = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
