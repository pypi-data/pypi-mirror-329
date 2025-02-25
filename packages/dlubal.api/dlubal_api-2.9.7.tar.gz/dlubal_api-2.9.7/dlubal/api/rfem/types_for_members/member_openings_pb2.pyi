from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberOpeningsComponentsReductionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_OPENINGS_COMPONENTS_REDUCTION_TYPE_REDUCTION_COMPONENT_TYPE_RECTANGLE_OPENING: _ClassVar[MemberOpeningsComponentsReductionType]
    MEMBER_OPENINGS_COMPONENTS_REDUCTION_TYPE_REDUCTION_COMPONENT_TYPE_CIRCLE_OPENING: _ClassVar[MemberOpeningsComponentsReductionType]
    MEMBER_OPENINGS_COMPONENTS_REDUCTION_TYPE_REDUCTION_COMPONENT_TYPE_HEXAGONAL_OPENING: _ClassVar[MemberOpeningsComponentsReductionType]

class MemberOpeningsComponentsMultipleOffsetDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_OPENINGS_COMPONENTS_MULTIPLE_OFFSET_DEFINITION_TYPE_ABSOLUTE: _ClassVar[MemberOpeningsComponentsMultipleOffsetDefinitionType]
    MEMBER_OPENINGS_COMPONENTS_MULTIPLE_OFFSET_DEFINITION_TYPE_RELATIVE: _ClassVar[MemberOpeningsComponentsMultipleOffsetDefinitionType]

class MemberOpeningsComponentsZAxisReferenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_OPENINGS_COMPONENTS_Z_AXIS_REFERENCE_TYPE_E_POSITION_REFERENCE_TOP: _ClassVar[MemberOpeningsComponentsZAxisReferenceType]
    MEMBER_OPENINGS_COMPONENTS_Z_AXIS_REFERENCE_TYPE_E_POSITION_REFERENCE_BOTTOM: _ClassVar[MemberOpeningsComponentsZAxisReferenceType]
    MEMBER_OPENINGS_COMPONENTS_Z_AXIS_REFERENCE_TYPE_E_POSITION_REFERENCE_CENTER: _ClassVar[MemberOpeningsComponentsZAxisReferenceType]
MEMBER_OPENINGS_COMPONENTS_REDUCTION_TYPE_REDUCTION_COMPONENT_TYPE_RECTANGLE_OPENING: MemberOpeningsComponentsReductionType
MEMBER_OPENINGS_COMPONENTS_REDUCTION_TYPE_REDUCTION_COMPONENT_TYPE_CIRCLE_OPENING: MemberOpeningsComponentsReductionType
MEMBER_OPENINGS_COMPONENTS_REDUCTION_TYPE_REDUCTION_COMPONENT_TYPE_HEXAGONAL_OPENING: MemberOpeningsComponentsReductionType
MEMBER_OPENINGS_COMPONENTS_MULTIPLE_OFFSET_DEFINITION_TYPE_ABSOLUTE: MemberOpeningsComponentsMultipleOffsetDefinitionType
MEMBER_OPENINGS_COMPONENTS_MULTIPLE_OFFSET_DEFINITION_TYPE_RELATIVE: MemberOpeningsComponentsMultipleOffsetDefinitionType
MEMBER_OPENINGS_COMPONENTS_Z_AXIS_REFERENCE_TYPE_E_POSITION_REFERENCE_TOP: MemberOpeningsComponentsZAxisReferenceType
MEMBER_OPENINGS_COMPONENTS_Z_AXIS_REFERENCE_TYPE_E_POSITION_REFERENCE_BOTTOM: MemberOpeningsComponentsZAxisReferenceType
MEMBER_OPENINGS_COMPONENTS_Z_AXIS_REFERENCE_TYPE_E_POSITION_REFERENCE_CENTER: MemberOpeningsComponentsZAxisReferenceType

class MemberOpenings(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "members", "member_sets", "components", "is_generated", "generating_object_info", "comment", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    members: _containers.RepeatedScalarFieldContainer[int]
    member_sets: _containers.RepeatedScalarFieldContainer[int]
    components: MemberOpeningsComponentsTable
    is_generated: bool
    generating_object_info: str
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., members: _Optional[_Iterable[int]] = ..., member_sets: _Optional[_Iterable[int]] = ..., components: _Optional[_Union[MemberOpeningsComponentsTable, _Mapping]] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class MemberOpeningsComponentsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[MemberOpeningsComponentsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[MemberOpeningsComponentsRow, _Mapping]]] = ...) -> None: ...

class MemberOpeningsComponentsRow(_message.Message):
    __slots__ = ("no", "description", "reduction_type", "position", "multiple", "note", "multiple_number", "multiple_offset_definition_type", "multiple_offset", "width", "height", "z_axis_reference_type", "distance", "diameter", "width_center")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REDUCTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_OFFSET_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    Z_AXIS_REFERENCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    DIAMETER_FIELD_NUMBER: _ClassVar[int]
    WIDTH_CENTER_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    reduction_type: MemberOpeningsComponentsReductionType
    position: float
    multiple: bool
    note: str
    multiple_number: int
    multiple_offset_definition_type: MemberOpeningsComponentsMultipleOffsetDefinitionType
    multiple_offset: float
    width: float
    height: float
    z_axis_reference_type: MemberOpeningsComponentsZAxisReferenceType
    distance: float
    diameter: float
    width_center: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., reduction_type: _Optional[_Union[MemberOpeningsComponentsReductionType, str]] = ..., position: _Optional[float] = ..., multiple: bool = ..., note: _Optional[str] = ..., multiple_number: _Optional[int] = ..., multiple_offset_definition_type: _Optional[_Union[MemberOpeningsComponentsMultipleOffsetDefinitionType, str]] = ..., multiple_offset: _Optional[float] = ..., width: _Optional[float] = ..., height: _Optional[float] = ..., z_axis_reference_type: _Optional[_Union[MemberOpeningsComponentsZAxisReferenceType, str]] = ..., distance: _Optional[float] = ..., diameter: _Optional[float] = ..., width_center: _Optional[float] = ...) -> None: ...
