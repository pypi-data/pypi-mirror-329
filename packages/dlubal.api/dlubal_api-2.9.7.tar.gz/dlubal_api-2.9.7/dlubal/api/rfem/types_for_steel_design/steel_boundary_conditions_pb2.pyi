from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SteelBoundaryConditionsDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STEEL_BOUNDARY_CONDITIONS_DEFINITION_TYPE_UNKNOWN: _ClassVar[SteelBoundaryConditionsDefinitionType]
    STEEL_BOUNDARY_CONDITIONS_DEFINITION_TYPE_2D: _ClassVar[SteelBoundaryConditionsDefinitionType]

class SteelBoundaryConditionsNodalSupportsSupportType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_NONE: _ClassVar[SteelBoundaryConditionsNodalSupportsSupportType]
    STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_ALL: _ClassVar[SteelBoundaryConditionsNodalSupportsSupportType]
    STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y: _ClassVar[SteelBoundaryConditionsNodalSupportsSupportType]
    STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y_AND_TORSION: _ClassVar[SteelBoundaryConditionsNodalSupportsSupportType]
    STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y_AND_TORSION_AND_WARPING: _ClassVar[SteelBoundaryConditionsNodalSupportsSupportType]
    STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y_AND_WARPING: _ClassVar[SteelBoundaryConditionsNodalSupportsSupportType]
    STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_INDIVIDUALLY: _ClassVar[SteelBoundaryConditionsNodalSupportsSupportType]
    STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_TORSION: _ClassVar[SteelBoundaryConditionsNodalSupportsSupportType]
    STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_TORSION_AND_WARPING: _ClassVar[SteelBoundaryConditionsNodalSupportsSupportType]

class SteelBoundaryConditionsNodalSupportsEccentricityTypeZType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_Z_TYPE_ECCENTRICITY_TYPE_NONE: _ClassVar[SteelBoundaryConditionsNodalSupportsEccentricityTypeZType]
    STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_Z_TYPE_ECCENTRICITY_TYPE_AT_LOWER_FLANGE: _ClassVar[SteelBoundaryConditionsNodalSupportsEccentricityTypeZType]
    STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_Z_TYPE_ECCENTRICITY_TYPE_AT_UPPER_FLANGE: _ClassVar[SteelBoundaryConditionsNodalSupportsEccentricityTypeZType]
    STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_Z_TYPE_ECCENTRICITY_TYPE_USER_VALUE: _ClassVar[SteelBoundaryConditionsNodalSupportsEccentricityTypeZType]
STEEL_BOUNDARY_CONDITIONS_DEFINITION_TYPE_UNKNOWN: SteelBoundaryConditionsDefinitionType
STEEL_BOUNDARY_CONDITIONS_DEFINITION_TYPE_2D: SteelBoundaryConditionsDefinitionType
STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_NONE: SteelBoundaryConditionsNodalSupportsSupportType
STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_ALL: SteelBoundaryConditionsNodalSupportsSupportType
STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y: SteelBoundaryConditionsNodalSupportsSupportType
STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y_AND_TORSION: SteelBoundaryConditionsNodalSupportsSupportType
STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y_AND_TORSION_AND_WARPING: SteelBoundaryConditionsNodalSupportsSupportType
STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y_AND_WARPING: SteelBoundaryConditionsNodalSupportsSupportType
STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_INDIVIDUALLY: SteelBoundaryConditionsNodalSupportsSupportType
STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_TORSION: SteelBoundaryConditionsNodalSupportsSupportType
STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_SUPPORT_TYPE_TORSION_AND_WARPING: SteelBoundaryConditionsNodalSupportsSupportType
STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_Z_TYPE_ECCENTRICITY_TYPE_NONE: SteelBoundaryConditionsNodalSupportsEccentricityTypeZType
STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_Z_TYPE_ECCENTRICITY_TYPE_AT_LOWER_FLANGE: SteelBoundaryConditionsNodalSupportsEccentricityTypeZType
STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_Z_TYPE_ECCENTRICITY_TYPE_AT_UPPER_FLANGE: SteelBoundaryConditionsNodalSupportsEccentricityTypeZType
STEEL_BOUNDARY_CONDITIONS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_Z_TYPE_ECCENTRICITY_TYPE_USER_VALUE: SteelBoundaryConditionsNodalSupportsEccentricityTypeZType

class SteelBoundaryConditions(_message.Message):
    __slots__ = ("no", "definition_type", "coordinate_system", "user_defined_name_enabled", "name", "comment", "members", "member_sets", "intermediate_nodes", "nodal_supports", "member_hinges", "different_properties_supports", "different_properties_hinges", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    INTERMEDIATE_NODES_FIELD_NUMBER: _ClassVar[int]
    NODAL_SUPPORTS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_HINGES_FIELD_NUMBER: _ClassVar[int]
    DIFFERENT_PROPERTIES_SUPPORTS_FIELD_NUMBER: _ClassVar[int]
    DIFFERENT_PROPERTIES_HINGES_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    definition_type: SteelBoundaryConditionsDefinitionType
    coordinate_system: str
    user_defined_name_enabled: bool
    name: str
    comment: str
    members: _containers.RepeatedScalarFieldContainer[int]
    member_sets: _containers.RepeatedScalarFieldContainer[int]
    intermediate_nodes: bool
    nodal_supports: SteelBoundaryConditionsNodalSupportsTable
    member_hinges: SteelBoundaryConditionsMemberHingesTable
    different_properties_supports: bool
    different_properties_hinges: bool
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., definition_type: _Optional[_Union[SteelBoundaryConditionsDefinitionType, str]] = ..., coordinate_system: _Optional[str] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., comment: _Optional[str] = ..., members: _Optional[_Iterable[int]] = ..., member_sets: _Optional[_Iterable[int]] = ..., intermediate_nodes: bool = ..., nodal_supports: _Optional[_Union[SteelBoundaryConditionsNodalSupportsTable, _Mapping]] = ..., member_hinges: _Optional[_Union[SteelBoundaryConditionsMemberHingesTable, _Mapping]] = ..., different_properties_supports: bool = ..., different_properties_hinges: bool = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class SteelBoundaryConditionsNodalSupportsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[SteelBoundaryConditionsNodalSupportsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[SteelBoundaryConditionsNodalSupportsRow, _Mapping]]] = ...) -> None: ...

class SteelBoundaryConditionsNodalSupportsRow(_message.Message):
    __slots__ = ("no", "description", "node_seq_no", "support_type", "support_in_x", "support_in_y", "support_in_z", "restraint_about_x", "restraint_about_y", "restraint_about_z", "restraint_warping", "rotation", "rotation_about_x", "rotation_about_y", "rotation_about_z", "support_spring_in_x", "support_spring_in_y", "support_spring_in_z", "restraint_spring_about_x", "restraint_spring_about_y", "restraint_spring_about_z", "restraint_spring_warping", "eccentricity_type_z_type", "eccentricity_x", "eccentricity_y", "eccentricity_z", "nodes")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NODE_SEQ_NO_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_IN_X_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_IN_Y_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_IN_Z_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_ABOUT_X_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_ABOUT_Y_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_WARPING_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ABOUT_X_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ABOUT_Y_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_SPRING_IN_X_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_SPRING_IN_Y_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_SPRING_IN_Z_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_SPRING_ABOUT_X_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_SPRING_ABOUT_Y_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_SPRING_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_SPRING_WARPING_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_TYPE_Z_TYPE_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_X_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_Y_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_Z_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    node_seq_no: str
    support_type: SteelBoundaryConditionsNodalSupportsSupportType
    support_in_x: bool
    support_in_y: bool
    support_in_z: bool
    restraint_about_x: bool
    restraint_about_y: bool
    restraint_about_z: bool
    restraint_warping: bool
    rotation: float
    rotation_about_x: float
    rotation_about_y: float
    rotation_about_z: float
    support_spring_in_x: float
    support_spring_in_y: float
    support_spring_in_z: float
    restraint_spring_about_x: float
    restraint_spring_about_y: float
    restraint_spring_about_z: float
    restraint_spring_warping: float
    eccentricity_type_z_type: SteelBoundaryConditionsNodalSupportsEccentricityTypeZType
    eccentricity_x: float
    eccentricity_y: float
    eccentricity_z: float
    nodes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., node_seq_no: _Optional[str] = ..., support_type: _Optional[_Union[SteelBoundaryConditionsNodalSupportsSupportType, str]] = ..., support_in_x: bool = ..., support_in_y: bool = ..., support_in_z: bool = ..., restraint_about_x: bool = ..., restraint_about_y: bool = ..., restraint_about_z: bool = ..., restraint_warping: bool = ..., rotation: _Optional[float] = ..., rotation_about_x: _Optional[float] = ..., rotation_about_y: _Optional[float] = ..., rotation_about_z: _Optional[float] = ..., support_spring_in_x: _Optional[float] = ..., support_spring_in_y: _Optional[float] = ..., support_spring_in_z: _Optional[float] = ..., restraint_spring_about_x: _Optional[float] = ..., restraint_spring_about_y: _Optional[float] = ..., restraint_spring_about_z: _Optional[float] = ..., restraint_spring_warping: _Optional[float] = ..., eccentricity_type_z_type: _Optional[_Union[SteelBoundaryConditionsNodalSupportsEccentricityTypeZType, str]] = ..., eccentricity_x: _Optional[float] = ..., eccentricity_y: _Optional[float] = ..., eccentricity_z: _Optional[float] = ..., nodes: _Optional[_Iterable[int]] = ...) -> None: ...

class SteelBoundaryConditionsMemberHingesTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[SteelBoundaryConditionsMemberHingesRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[SteelBoundaryConditionsMemberHingesRow, _Mapping]]] = ...) -> None: ...

class SteelBoundaryConditionsMemberHingesRow(_message.Message):
    __slots__ = ("no", "description", "node_seq_no", "release_in_x", "release_in_y", "release_in_z", "release_about_x", "release_about_y", "release_about_z", "release_warping", "release_spring_in_x", "release_spring_in_y", "release_spring_in_z", "release_spring_about_x", "release_spring_about_y", "release_spring_about_z", "release_spring_warping", "nodes")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NODE_SEQ_NO_FIELD_NUMBER: _ClassVar[int]
    RELEASE_IN_X_FIELD_NUMBER: _ClassVar[int]
    RELEASE_IN_Y_FIELD_NUMBER: _ClassVar[int]
    RELEASE_IN_Z_FIELD_NUMBER: _ClassVar[int]
    RELEASE_ABOUT_X_FIELD_NUMBER: _ClassVar[int]
    RELEASE_ABOUT_Y_FIELD_NUMBER: _ClassVar[int]
    RELEASE_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
    RELEASE_WARPING_FIELD_NUMBER: _ClassVar[int]
    RELEASE_SPRING_IN_X_FIELD_NUMBER: _ClassVar[int]
    RELEASE_SPRING_IN_Y_FIELD_NUMBER: _ClassVar[int]
    RELEASE_SPRING_IN_Z_FIELD_NUMBER: _ClassVar[int]
    RELEASE_SPRING_ABOUT_X_FIELD_NUMBER: _ClassVar[int]
    RELEASE_SPRING_ABOUT_Y_FIELD_NUMBER: _ClassVar[int]
    RELEASE_SPRING_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
    RELEASE_SPRING_WARPING_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    node_seq_no: str
    release_in_x: bool
    release_in_y: bool
    release_in_z: bool
    release_about_x: bool
    release_about_y: bool
    release_about_z: bool
    release_warping: bool
    release_spring_in_x: float
    release_spring_in_y: float
    release_spring_in_z: float
    release_spring_about_x: float
    release_spring_about_y: float
    release_spring_about_z: float
    release_spring_warping: float
    nodes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., node_seq_no: _Optional[str] = ..., release_in_x: bool = ..., release_in_y: bool = ..., release_in_z: bool = ..., release_about_x: bool = ..., release_about_y: bool = ..., release_about_z: bool = ..., release_warping: bool = ..., release_spring_in_x: _Optional[float] = ..., release_spring_in_y: _Optional[float] = ..., release_spring_in_z: _Optional[float] = ..., release_spring_about_x: _Optional[float] = ..., release_spring_about_y: _Optional[float] = ..., release_spring_about_z: _Optional[float] = ..., release_spring_warping: _Optional[float] = ..., nodes: _Optional[_Iterable[int]] = ...) -> None: ...
