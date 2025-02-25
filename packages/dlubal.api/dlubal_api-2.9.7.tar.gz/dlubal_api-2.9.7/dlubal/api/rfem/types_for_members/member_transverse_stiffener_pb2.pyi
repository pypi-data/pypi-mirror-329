from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberTransverseStiffenerComponentsStiffenerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_FLAT: _ClassVar[MemberTransverseStiffenerComponentsStiffenerType]
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_ANGLE: _ClassVar[MemberTransverseStiffenerComponentsStiffenerType]
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_CHANNEL_SECTION: _ClassVar[MemberTransverseStiffenerComponentsStiffenerType]
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_CONNECTING_COLUMN_END: _ClassVar[MemberTransverseStiffenerComponentsStiffenerType]
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_CONNECTING_COLUMN_START: _ClassVar[MemberTransverseStiffenerComponentsStiffenerType]
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_END_PLATE_END: _ClassVar[MemberTransverseStiffenerComponentsStiffenerType]
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_END_PLATE_START: _ClassVar[MemberTransverseStiffenerComponentsStiffenerType]
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_WARPING_RESTRAINT: _ClassVar[MemberTransverseStiffenerComponentsStiffenerType]

class MemberTransverseStiffenerComponentsPositionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_POSITION_TYPE_STIFFENER_COMPONENT_POSITION_DOUBLE_SIDED: _ClassVar[MemberTransverseStiffenerComponentsPositionType]
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_POSITION_TYPE_STIFFENER_COMPONENT_POSITION_SINGLE_SIDED_LEFT: _ClassVar[MemberTransverseStiffenerComponentsPositionType]
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_POSITION_TYPE_STIFFENER_COMPONENT_POSITION_SINGLE_SIDED_RIGHT: _ClassVar[MemberTransverseStiffenerComponentsPositionType]

class MemberTransverseStiffenerComponentsMultipleOffsetDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_MULTIPLE_OFFSET_DEFINITION_TYPE_ABSOLUTE: _ClassVar[MemberTransverseStiffenerComponentsMultipleOffsetDefinitionType]
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_MULTIPLE_OFFSET_DEFINITION_TYPE_RELATIVE: _ClassVar[MemberTransverseStiffenerComponentsMultipleOffsetDefinitionType]

class MemberTransverseStiffenerComponentsDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_DEFINITION_TYPE_DIMENSION_TYPE_OFFSET: _ClassVar[MemberTransverseStiffenerComponentsDefinitionType]
    MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_DEFINITION_TYPE_DIMENSION_TYPE_SIZE: _ClassVar[MemberTransverseStiffenerComponentsDefinitionType]
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_FLAT: MemberTransverseStiffenerComponentsStiffenerType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_ANGLE: MemberTransverseStiffenerComponentsStiffenerType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_CHANNEL_SECTION: MemberTransverseStiffenerComponentsStiffenerType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_CONNECTING_COLUMN_END: MemberTransverseStiffenerComponentsStiffenerType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_CONNECTING_COLUMN_START: MemberTransverseStiffenerComponentsStiffenerType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_END_PLATE_END: MemberTransverseStiffenerComponentsStiffenerType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_END_PLATE_START: MemberTransverseStiffenerComponentsStiffenerType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_STIFFENER_TYPE_STIFFENER_COMPONENT_TYPE_WARPING_RESTRAINT: MemberTransverseStiffenerComponentsStiffenerType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_POSITION_TYPE_STIFFENER_COMPONENT_POSITION_DOUBLE_SIDED: MemberTransverseStiffenerComponentsPositionType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_POSITION_TYPE_STIFFENER_COMPONENT_POSITION_SINGLE_SIDED_LEFT: MemberTransverseStiffenerComponentsPositionType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_POSITION_TYPE_STIFFENER_COMPONENT_POSITION_SINGLE_SIDED_RIGHT: MemberTransverseStiffenerComponentsPositionType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_MULTIPLE_OFFSET_DEFINITION_TYPE_ABSOLUTE: MemberTransverseStiffenerComponentsMultipleOffsetDefinitionType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_MULTIPLE_OFFSET_DEFINITION_TYPE_RELATIVE: MemberTransverseStiffenerComponentsMultipleOffsetDefinitionType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_DEFINITION_TYPE_DIMENSION_TYPE_OFFSET: MemberTransverseStiffenerComponentsDefinitionType
MEMBER_TRANSVERSE_STIFFENER_COMPONENTS_DEFINITION_TYPE_DIMENSION_TYPE_SIZE: MemberTransverseStiffenerComponentsDefinitionType

class MemberTransverseStiffener(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "members", "member_sets", "components", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    members: _containers.RepeatedScalarFieldContainer[int]
    member_sets: _containers.RepeatedScalarFieldContainer[int]
    components: MemberTransverseStiffenerComponentsTable
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., members: _Optional[_Iterable[int]] = ..., member_sets: _Optional[_Iterable[int]] = ..., components: _Optional[_Union[MemberTransverseStiffenerComponentsTable, _Mapping]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class MemberTransverseStiffenerComponentsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[MemberTransverseStiffenerComponentsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[MemberTransverseStiffenerComponentsRow, _Mapping]]] = ...) -> None: ...

class MemberTransverseStiffenerComponentsRow(_message.Message):
    __slots__ = ("no", "description", "stiffener_type", "position", "position_type", "multiple", "note", "multiple_number", "multiple_offset_definition_type", "multiple_offset", "material", "consider_stiffener", "definition_type", "offset_horizontal", "offset_vertical", "thickness", "width", "height", "non_rigid", "rigid", "width_b_u", "height_h_u", "thickness_t_u", "thickness_s_u", "width_b", "thickness_t", "column_section", "section", "cantilever_l_c", "full_warping_restraint", "user_defined_restraint", "user_defined_restraint_value")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STIFFENER_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    POSITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_OFFSET_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_STIFFENER_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_HORIZONTAL_FIELD_NUMBER: _ClassVar[int]
    OFFSET_VERTICAL_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    NON_RIGID_FIELD_NUMBER: _ClassVar[int]
    RIGID_FIELD_NUMBER: _ClassVar[int]
    WIDTH_B_U_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_H_U_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_T_U_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_S_U_FIELD_NUMBER: _ClassVar[int]
    WIDTH_B_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_T_FIELD_NUMBER: _ClassVar[int]
    COLUMN_SECTION_FIELD_NUMBER: _ClassVar[int]
    SECTION_FIELD_NUMBER: _ClassVar[int]
    CANTILEVER_L_C_FIELD_NUMBER: _ClassVar[int]
    FULL_WARPING_RESTRAINT_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_RESTRAINT_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_RESTRAINT_VALUE_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    stiffener_type: MemberTransverseStiffenerComponentsStiffenerType
    position: float
    position_type: MemberTransverseStiffenerComponentsPositionType
    multiple: bool
    note: str
    multiple_number: int
    multiple_offset_definition_type: MemberTransverseStiffenerComponentsMultipleOffsetDefinitionType
    multiple_offset: float
    material: int
    consider_stiffener: bool
    definition_type: MemberTransverseStiffenerComponentsDefinitionType
    offset_horizontal: float
    offset_vertical: float
    thickness: float
    width: float
    height: float
    non_rigid: bool
    rigid: bool
    width_b_u: float
    height_h_u: float
    thickness_t_u: float
    thickness_s_u: float
    width_b: float
    thickness_t: float
    column_section: int
    section: int
    cantilever_l_c: float
    full_warping_restraint: bool
    user_defined_restraint: bool
    user_defined_restraint_value: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., stiffener_type: _Optional[_Union[MemberTransverseStiffenerComponentsStiffenerType, str]] = ..., position: _Optional[float] = ..., position_type: _Optional[_Union[MemberTransverseStiffenerComponentsPositionType, str]] = ..., multiple: bool = ..., note: _Optional[str] = ..., multiple_number: _Optional[int] = ..., multiple_offset_definition_type: _Optional[_Union[MemberTransverseStiffenerComponentsMultipleOffsetDefinitionType, str]] = ..., multiple_offset: _Optional[float] = ..., material: _Optional[int] = ..., consider_stiffener: bool = ..., definition_type: _Optional[_Union[MemberTransverseStiffenerComponentsDefinitionType, str]] = ..., offset_horizontal: _Optional[float] = ..., offset_vertical: _Optional[float] = ..., thickness: _Optional[float] = ..., width: _Optional[float] = ..., height: _Optional[float] = ..., non_rigid: bool = ..., rigid: bool = ..., width_b_u: _Optional[float] = ..., height_h_u: _Optional[float] = ..., thickness_t_u: _Optional[float] = ..., thickness_s_u: _Optional[float] = ..., width_b: _Optional[float] = ..., thickness_t: _Optional[float] = ..., column_section: _Optional[int] = ..., section: _Optional[int] = ..., cantilever_l_c: _Optional[float] = ..., full_warping_restraint: bool = ..., user_defined_restraint: bool = ..., user_defined_restraint_value: _Optional[float] = ...) -> None: ...
