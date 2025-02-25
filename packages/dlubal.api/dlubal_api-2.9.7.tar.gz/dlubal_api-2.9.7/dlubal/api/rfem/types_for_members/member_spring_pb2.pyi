from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberSpringDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_SPRING_DEFINITION_TYPE_UNKNOWN: _ClassVar[MemberSpringDefinitionType]
    MEMBER_SPRING_DEFINITION_TYPE_DIAGRAM: _ClassVar[MemberSpringDefinitionType]
    MEMBER_SPRING_DEFINITION_TYPE_PARTIAL_ACTIVITY: _ClassVar[MemberSpringDefinitionType]

class MemberSpringSelfWeightDefinition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_SPRING_SELF_WEIGHT_DEFINITION_MASS: _ClassVar[MemberSpringSelfWeightDefinition]
    MEMBER_SPRING_SELF_WEIGHT_DEFINITION_MASS_PER_LENGTH: _ClassVar[MemberSpringSelfWeightDefinition]
    MEMBER_SPRING_SELF_WEIGHT_DEFINITION_SPECIFIC_WEIGHT: _ClassVar[MemberSpringSelfWeightDefinition]

class MemberSpringPartialActivityAlongXNegativeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_PARTIAL_ACTIVITY_TYPE_COMPLETE: _ClassVar[MemberSpringPartialActivityAlongXNegativeType]
    MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_PARTIAL_ACTIVITY_TYPE_FAILURE_FROM_FORCE: _ClassVar[MemberSpringPartialActivityAlongXNegativeType]
    MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_PARTIAL_ACTIVITY_TYPE_FIXED: _ClassVar[MemberSpringPartialActivityAlongXNegativeType]
    MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_PARTIAL_ACTIVITY_TYPE_INEFFECTIVNESS: _ClassVar[MemberSpringPartialActivityAlongXNegativeType]
    MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_PARTIAL_ACTIVITY_TYPE_YIELDING_FROM_FORCE: _ClassVar[MemberSpringPartialActivityAlongXNegativeType]

class MemberSpringPartialActivityAlongXPositiveType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_PARTIAL_ACTIVITY_TYPE_COMPLETE: _ClassVar[MemberSpringPartialActivityAlongXPositiveType]
    MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_PARTIAL_ACTIVITY_TYPE_FAILURE_FROM_FORCE: _ClassVar[MemberSpringPartialActivityAlongXPositiveType]
    MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_PARTIAL_ACTIVITY_TYPE_FIXED: _ClassVar[MemberSpringPartialActivityAlongXPositiveType]
    MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_PARTIAL_ACTIVITY_TYPE_INEFFECTIVNESS: _ClassVar[MemberSpringPartialActivityAlongXPositiveType]
    MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_PARTIAL_ACTIVITY_TYPE_YIELDING_FROM_FORCE: _ClassVar[MemberSpringPartialActivityAlongXPositiveType]

class MemberSpringDiagramAlongXStart(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_SPRING_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_FAILURE: _ClassVar[MemberSpringDiagramAlongXStart]
    MEMBER_SPRING_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_CONTINUOUS: _ClassVar[MemberSpringDiagramAlongXStart]
    MEMBER_SPRING_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_STOP: _ClassVar[MemberSpringDiagramAlongXStart]
    MEMBER_SPRING_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_YIELDING: _ClassVar[MemberSpringDiagramAlongXStart]

class MemberSpringDiagramAlongXEnd(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_SPRING_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_FAILURE: _ClassVar[MemberSpringDiagramAlongXEnd]
    MEMBER_SPRING_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_CONTINUOUS: _ClassVar[MemberSpringDiagramAlongXEnd]
    MEMBER_SPRING_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_STOP: _ClassVar[MemberSpringDiagramAlongXEnd]
    MEMBER_SPRING_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_YIELDING: _ClassVar[MemberSpringDiagramAlongXEnd]
MEMBER_SPRING_DEFINITION_TYPE_UNKNOWN: MemberSpringDefinitionType
MEMBER_SPRING_DEFINITION_TYPE_DIAGRAM: MemberSpringDefinitionType
MEMBER_SPRING_DEFINITION_TYPE_PARTIAL_ACTIVITY: MemberSpringDefinitionType
MEMBER_SPRING_SELF_WEIGHT_DEFINITION_MASS: MemberSpringSelfWeightDefinition
MEMBER_SPRING_SELF_WEIGHT_DEFINITION_MASS_PER_LENGTH: MemberSpringSelfWeightDefinition
MEMBER_SPRING_SELF_WEIGHT_DEFINITION_SPECIFIC_WEIGHT: MemberSpringSelfWeightDefinition
MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_PARTIAL_ACTIVITY_TYPE_COMPLETE: MemberSpringPartialActivityAlongXNegativeType
MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_PARTIAL_ACTIVITY_TYPE_FAILURE_FROM_FORCE: MemberSpringPartialActivityAlongXNegativeType
MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_PARTIAL_ACTIVITY_TYPE_FIXED: MemberSpringPartialActivityAlongXNegativeType
MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_PARTIAL_ACTIVITY_TYPE_INEFFECTIVNESS: MemberSpringPartialActivityAlongXNegativeType
MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_PARTIAL_ACTIVITY_TYPE_YIELDING_FROM_FORCE: MemberSpringPartialActivityAlongXNegativeType
MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_PARTIAL_ACTIVITY_TYPE_COMPLETE: MemberSpringPartialActivityAlongXPositiveType
MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_PARTIAL_ACTIVITY_TYPE_FAILURE_FROM_FORCE: MemberSpringPartialActivityAlongXPositiveType
MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_PARTIAL_ACTIVITY_TYPE_FIXED: MemberSpringPartialActivityAlongXPositiveType
MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_PARTIAL_ACTIVITY_TYPE_INEFFECTIVNESS: MemberSpringPartialActivityAlongXPositiveType
MEMBER_SPRING_PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_PARTIAL_ACTIVITY_TYPE_YIELDING_FROM_FORCE: MemberSpringPartialActivityAlongXPositiveType
MEMBER_SPRING_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_FAILURE: MemberSpringDiagramAlongXStart
MEMBER_SPRING_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_CONTINUOUS: MemberSpringDiagramAlongXStart
MEMBER_SPRING_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_STOP: MemberSpringDiagramAlongXStart
MEMBER_SPRING_DIAGRAM_ALONG_X_START_DIAGRAM_ENDING_TYPE_YIELDING: MemberSpringDiagramAlongXStart
MEMBER_SPRING_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_FAILURE: MemberSpringDiagramAlongXEnd
MEMBER_SPRING_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_CONTINUOUS: MemberSpringDiagramAlongXEnd
MEMBER_SPRING_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_STOP: MemberSpringDiagramAlongXEnd
MEMBER_SPRING_DIAGRAM_ALONG_X_END_DIAGRAM_ENDING_TYPE_YIELDING: MemberSpringDiagramAlongXEnd

class MemberSpring(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_to", "definition_type", "axial_stiffness", "self_weight_definition", "mass", "mass_per_length", "specific_weight", "section_area", "partial_activity_along_x_negative_type", "partial_activity_along_x_negative_displacement", "partial_activity_along_x_negative_force", "partial_activity_along_x_negative_slippage", "partial_activity_along_x_positive_type", "partial_activity_along_x_positive_displacement", "partial_activity_along_x_positive_force", "partial_activity_along_x_positive_slippage", "diagram_along_x_symmetric", "diagram_along_x_is_sorted", "diagram_along_x_table", "diagram_along_x_start", "diagram_along_x_end", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    AXIAL_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
    SELF_WEIGHT_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    MASS_FIELD_NUMBER: _ClassVar[int]
    MASS_PER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SPECIFIC_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    SECTION_AREA_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_FORCE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_POSITIVE_DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_POSITIVE_FORCE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_POSITIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_IS_SORTED_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_START_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_END_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    assigned_to: _containers.RepeatedScalarFieldContainer[int]
    definition_type: MemberSpringDefinitionType
    axial_stiffness: float
    self_weight_definition: MemberSpringSelfWeightDefinition
    mass: float
    mass_per_length: float
    specific_weight: float
    section_area: float
    partial_activity_along_x_negative_type: MemberSpringPartialActivityAlongXNegativeType
    partial_activity_along_x_negative_displacement: float
    partial_activity_along_x_negative_force: float
    partial_activity_along_x_negative_slippage: float
    partial_activity_along_x_positive_type: MemberSpringPartialActivityAlongXPositiveType
    partial_activity_along_x_positive_displacement: float
    partial_activity_along_x_positive_force: float
    partial_activity_along_x_positive_slippage: float
    diagram_along_x_symmetric: bool
    diagram_along_x_is_sorted: bool
    diagram_along_x_table: MemberSpringDiagramAlongXTable
    diagram_along_x_start: MemberSpringDiagramAlongXStart
    diagram_along_x_end: MemberSpringDiagramAlongXEnd
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to: _Optional[_Iterable[int]] = ..., definition_type: _Optional[_Union[MemberSpringDefinitionType, str]] = ..., axial_stiffness: _Optional[float] = ..., self_weight_definition: _Optional[_Union[MemberSpringSelfWeightDefinition, str]] = ..., mass: _Optional[float] = ..., mass_per_length: _Optional[float] = ..., specific_weight: _Optional[float] = ..., section_area: _Optional[float] = ..., partial_activity_along_x_negative_type: _Optional[_Union[MemberSpringPartialActivityAlongXNegativeType, str]] = ..., partial_activity_along_x_negative_displacement: _Optional[float] = ..., partial_activity_along_x_negative_force: _Optional[float] = ..., partial_activity_along_x_negative_slippage: _Optional[float] = ..., partial_activity_along_x_positive_type: _Optional[_Union[MemberSpringPartialActivityAlongXPositiveType, str]] = ..., partial_activity_along_x_positive_displacement: _Optional[float] = ..., partial_activity_along_x_positive_force: _Optional[float] = ..., partial_activity_along_x_positive_slippage: _Optional[float] = ..., diagram_along_x_symmetric: bool = ..., diagram_along_x_is_sorted: bool = ..., diagram_along_x_table: _Optional[_Union[MemberSpringDiagramAlongXTable, _Mapping]] = ..., diagram_along_x_start: _Optional[_Union[MemberSpringDiagramAlongXStart, str]] = ..., diagram_along_x_end: _Optional[_Union[MemberSpringDiagramAlongXEnd, str]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class MemberSpringDiagramAlongXTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[MemberSpringDiagramAlongXTableRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[MemberSpringDiagramAlongXTableRow, _Mapping]]] = ...) -> None: ...

class MemberSpringDiagramAlongXTableRow(_message.Message):
    __slots__ = ("no", "description", "displacement", "force", "spring", "note")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    SPRING_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    displacement: float
    force: float
    spring: float
    note: str
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., displacement: _Optional[float] = ..., force: _Optional[float] = ..., spring: _Optional[float] = ..., note: _Optional[str] = ...) -> None: ...
