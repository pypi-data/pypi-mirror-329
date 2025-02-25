from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PunchingReinforcementType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PUNCHING_REINFORCEMENT_TYPE_UNKNOWN: _ClassVar[PunchingReinforcementType]
    PUNCHING_REINFORCEMENT_TYPE_HEADED_SHEAR_STUD: _ClassVar[PunchingReinforcementType]
    PUNCHING_REINFORCEMENT_TYPE_VERTICAL: _ClassVar[PunchingReinforcementType]

class PunchingReinforcementPlacementType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PUNCHING_REINFORCEMENT_PLACEMENT_TYPE_RADIAL: _ClassVar[PunchingReinforcementPlacementType]
    PUNCHING_REINFORCEMENT_PLACEMENT_TYPE_AXIAL: _ClassVar[PunchingReinforcementPlacementType]

class PunchingReinforcementPerimeterSpacingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PUNCHING_REINFORCEMENT_PERIMETER_SPACING_TYPE_MULTIPLE_STATIC_DEPTH: _ClassVar[PunchingReinforcementPerimeterSpacingType]
    PUNCHING_REINFORCEMENT_PERIMETER_SPACING_TYPE_ABSOLUTE: _ClassVar[PunchingReinforcementPerimeterSpacingType]

class PunchingReinforcementDifferentPlacementPerimeterSpacingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PUNCHING_REINFORCEMENT_DIFFERENT_PLACEMENT_PERIMETER_SPACING_TYPE_MULTIPLE_STATIC_DEPTH: _ClassVar[PunchingReinforcementDifferentPlacementPerimeterSpacingType]
    PUNCHING_REINFORCEMENT_DIFFERENT_PLACEMENT_PERIMETER_SPACING_TYPE_ABSOLUTE: _ClassVar[PunchingReinforcementDifferentPlacementPerimeterSpacingType]

class PunchingReinforcementBendUpSizeDesignation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PUNCHING_REINFORCEMENT_BEND_UP_SIZE_DESIGNATION_UNKNOWN: _ClassVar[PunchingReinforcementBendUpSizeDesignation]

class PunchingReinforcementBendUpSizeDesignationAutoMaximum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PUNCHING_REINFORCEMENT_BEND_UP_SIZE_DESIGNATION_AUTO_MAXIMUM_UNKNOWN: _ClassVar[PunchingReinforcementBendUpSizeDesignationAutoMaximum]

class PunchingReinforcementBendUpSizeDesignationAutoMinimum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PUNCHING_REINFORCEMENT_BEND_UP_SIZE_DESIGNATION_AUTO_MINIMUM_UNKNOWN: _ClassVar[PunchingReinforcementBendUpSizeDesignationAutoMinimum]
PUNCHING_REINFORCEMENT_TYPE_UNKNOWN: PunchingReinforcementType
PUNCHING_REINFORCEMENT_TYPE_HEADED_SHEAR_STUD: PunchingReinforcementType
PUNCHING_REINFORCEMENT_TYPE_VERTICAL: PunchingReinforcementType
PUNCHING_REINFORCEMENT_PLACEMENT_TYPE_RADIAL: PunchingReinforcementPlacementType
PUNCHING_REINFORCEMENT_PLACEMENT_TYPE_AXIAL: PunchingReinforcementPlacementType
PUNCHING_REINFORCEMENT_PERIMETER_SPACING_TYPE_MULTIPLE_STATIC_DEPTH: PunchingReinforcementPerimeterSpacingType
PUNCHING_REINFORCEMENT_PERIMETER_SPACING_TYPE_ABSOLUTE: PunchingReinforcementPerimeterSpacingType
PUNCHING_REINFORCEMENT_DIFFERENT_PLACEMENT_PERIMETER_SPACING_TYPE_MULTIPLE_STATIC_DEPTH: PunchingReinforcementDifferentPlacementPerimeterSpacingType
PUNCHING_REINFORCEMENT_DIFFERENT_PLACEMENT_PERIMETER_SPACING_TYPE_ABSOLUTE: PunchingReinforcementDifferentPlacementPerimeterSpacingType
PUNCHING_REINFORCEMENT_BEND_UP_SIZE_DESIGNATION_UNKNOWN: PunchingReinforcementBendUpSizeDesignation
PUNCHING_REINFORCEMENT_BEND_UP_SIZE_DESIGNATION_AUTO_MAXIMUM_UNKNOWN: PunchingReinforcementBendUpSizeDesignationAutoMaximum
PUNCHING_REINFORCEMENT_BEND_UP_SIZE_DESIGNATION_AUTO_MINIMUM_UNKNOWN: PunchingReinforcementBendUpSizeDesignationAutoMinimum

class PunchingReinforcement(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "nodes", "material", "placement_type", "number_of_perimeters", "number_of_perimeters_auto_enabled", "number_of_legs_in_each_perimeter", "number_of_legs_in_each_perimeter_auto_enabled", "perimeter_spacing_type", "multiple_static_depth_spacing_between_support_face_and_first_perimeter", "multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_enabled", "multiple_static_depth_spacing_between_perimeters", "multiple_static_depth_spacing_between_perimeters_auto_enabled", "absolute_spacing_between_support_face_and_first_perimeter", "absolute_spacing_between_support_face_and_first_perimeter_auto_enabled", "absolute_spacing_between_perimeters", "absolute_spacing_between_perimeters_auto_enabled", "bend_up_diameter", "bend_up_diameter_auto_enabled", "perimeter_area", "total_area", "integrated_in_surfaces", "comment", "is_generated", "generating_object_info", "number_of_perimeters_auto_maximum", "number_of_perimeters_auto_minimum", "number_of_perimeters_auto_priority", "number_of_perimeters_calculated", "number_of_legs_in_each_perimeter_auto_maximum", "number_of_legs_in_each_perimeter_auto_minimum", "number_of_legs_in_each_perimeter_auto_priority", "number_of_legs_in_each_perimeter_calculated", "multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_increment", "multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_maximum", "multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_minimum", "multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_priority", "multiple_static_depth_spacing_between_support_face_and_first_perimeter_calculated", "multiple_static_depth_spacing_between_perimeters_auto_increment", "multiple_static_depth_spacing_between_perimeters_auto_maximum", "multiple_static_depth_spacing_between_perimeters_auto_minimum", "multiple_static_depth_spacing_between_perimeters_auto_priority", "multiple_static_depth_spacing_between_perimeters_calculated", "different_placement_perimeters", "different_placement_perimeter_spacing_type", "bend_up_diameter_auto_maximum", "bend_up_diameter_auto_minimum", "bend_up_diameter_auto_priority", "bend_up_diameter_calculated", "bend_up_size_designation", "bend_up_size_designation_auto_maximum", "bend_up_size_designation_auto_minimum", "bend_up_diameter_auto_diameters_list", "bend_up_diameter_auto_diameters_list_enabled", "absolute_spacing_between_support_face_and_first_perimeter_auto_increment", "absolute_spacing_between_support_face_and_first_perimeter_auto_maximum", "absolute_spacing_between_support_face_and_first_perimeter_auto_minimum", "absolute_spacing_between_support_face_and_first_perimeter_auto_priority", "absolute_spacing_between_support_face_and_first_perimeter_calculated", "absolute_spacing_between_perimeters_auto_increment", "absolute_spacing_between_perimeters_auto_maximum", "absolute_spacing_between_perimeters_auto_minimum", "absolute_spacing_between_perimeters_auto_priority", "absolute_spacing_between_perimeters_calculated", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_FIELD_NUMBER: _ClassVar[int]
    PLACEMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_PERIMETERS_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_PERIMETERS_AUTO_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_LEGS_IN_EACH_PERIMETER_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_LEGS_IN_EACH_PERIMETER_AUTO_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PERIMETER_SPACING_TYPE_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_AUTO_ENABLED_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_PERIMETERS_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_PERIMETERS_AUTO_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_AUTO_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_PERIMETERS_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_PERIMETERS_AUTO_ENABLED_FIELD_NUMBER: _ClassVar[int]
    BEND_UP_DIAMETER_FIELD_NUMBER: _ClassVar[int]
    BEND_UP_DIAMETER_AUTO_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PERIMETER_AREA_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AREA_FIELD_NUMBER: _ClassVar[int]
    INTEGRATED_IN_SURFACES_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_PERIMETERS_AUTO_MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_PERIMETERS_AUTO_MINIMUM_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_PERIMETERS_AUTO_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_PERIMETERS_CALCULATED_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_LEGS_IN_EACH_PERIMETER_AUTO_MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_LEGS_IN_EACH_PERIMETER_AUTO_MINIMUM_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_LEGS_IN_EACH_PERIMETER_AUTO_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_LEGS_IN_EACH_PERIMETER_CALCULATED_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_AUTO_INCREMENT_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_AUTO_MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_AUTO_MINIMUM_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_AUTO_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_CALCULATED_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_PERIMETERS_AUTO_INCREMENT_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_PERIMETERS_AUTO_MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_PERIMETERS_AUTO_MINIMUM_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_PERIMETERS_AUTO_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_STATIC_DEPTH_SPACING_BETWEEN_PERIMETERS_CALCULATED_FIELD_NUMBER: _ClassVar[int]
    DIFFERENT_PLACEMENT_PERIMETERS_FIELD_NUMBER: _ClassVar[int]
    DIFFERENT_PLACEMENT_PERIMETER_SPACING_TYPE_FIELD_NUMBER: _ClassVar[int]
    BEND_UP_DIAMETER_AUTO_MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    BEND_UP_DIAMETER_AUTO_MINIMUM_FIELD_NUMBER: _ClassVar[int]
    BEND_UP_DIAMETER_AUTO_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    BEND_UP_DIAMETER_CALCULATED_FIELD_NUMBER: _ClassVar[int]
    BEND_UP_SIZE_DESIGNATION_FIELD_NUMBER: _ClassVar[int]
    BEND_UP_SIZE_DESIGNATION_AUTO_MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    BEND_UP_SIZE_DESIGNATION_AUTO_MINIMUM_FIELD_NUMBER: _ClassVar[int]
    BEND_UP_DIAMETER_AUTO_DIAMETERS_LIST_FIELD_NUMBER: _ClassVar[int]
    BEND_UP_DIAMETER_AUTO_DIAMETERS_LIST_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_AUTO_INCREMENT_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_AUTO_MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_AUTO_MINIMUM_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_AUTO_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_SUPPORT_FACE_AND_FIRST_PERIMETER_CALCULATED_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_PERIMETERS_AUTO_INCREMENT_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_PERIMETERS_AUTO_MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_PERIMETERS_AUTO_MINIMUM_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_PERIMETERS_AUTO_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SPACING_BETWEEN_PERIMETERS_CALCULATED_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: PunchingReinforcementType
    user_defined_name_enabled: bool
    name: str
    nodes: _containers.RepeatedScalarFieldContainer[int]
    material: int
    placement_type: PunchingReinforcementPlacementType
    number_of_perimeters: int
    number_of_perimeters_auto_enabled: bool
    number_of_legs_in_each_perimeter: int
    number_of_legs_in_each_perimeter_auto_enabled: bool
    perimeter_spacing_type: PunchingReinforcementPerimeterSpacingType
    multiple_static_depth_spacing_between_support_face_and_first_perimeter: float
    multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_enabled: bool
    multiple_static_depth_spacing_between_perimeters: float
    multiple_static_depth_spacing_between_perimeters_auto_enabled: bool
    absolute_spacing_between_support_face_and_first_perimeter: float
    absolute_spacing_between_support_face_and_first_perimeter_auto_enabled: bool
    absolute_spacing_between_perimeters: float
    absolute_spacing_between_perimeters_auto_enabled: bool
    bend_up_diameter: float
    bend_up_diameter_auto_enabled: bool
    perimeter_area: float
    total_area: float
    integrated_in_surfaces: _containers.RepeatedScalarFieldContainer[int]
    comment: str
    is_generated: bool
    generating_object_info: str
    number_of_perimeters_auto_maximum: int
    number_of_perimeters_auto_minimum: int
    number_of_perimeters_auto_priority: int
    number_of_perimeters_calculated: int
    number_of_legs_in_each_perimeter_auto_maximum: int
    number_of_legs_in_each_perimeter_auto_minimum: int
    number_of_legs_in_each_perimeter_auto_priority: int
    number_of_legs_in_each_perimeter_calculated: int
    multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_increment: float
    multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_maximum: float
    multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_minimum: float
    multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_priority: int
    multiple_static_depth_spacing_between_support_face_and_first_perimeter_calculated: float
    multiple_static_depth_spacing_between_perimeters_auto_increment: float
    multiple_static_depth_spacing_between_perimeters_auto_maximum: float
    multiple_static_depth_spacing_between_perimeters_auto_minimum: float
    multiple_static_depth_spacing_between_perimeters_auto_priority: int
    multiple_static_depth_spacing_between_perimeters_calculated: float
    different_placement_perimeters: PunchingReinforcementDifferentPlacementPerimetersTable
    different_placement_perimeter_spacing_type: PunchingReinforcementDifferentPlacementPerimeterSpacingType
    bend_up_diameter_auto_maximum: float
    bend_up_diameter_auto_minimum: float
    bend_up_diameter_auto_priority: int
    bend_up_diameter_calculated: float
    bend_up_size_designation: PunchingReinforcementBendUpSizeDesignation
    bend_up_size_designation_auto_maximum: PunchingReinforcementBendUpSizeDesignationAutoMaximum
    bend_up_size_designation_auto_minimum: PunchingReinforcementBendUpSizeDesignationAutoMinimum
    bend_up_diameter_auto_diameters_list: _containers.RepeatedScalarFieldContainer[int]
    bend_up_diameter_auto_diameters_list_enabled: bool
    absolute_spacing_between_support_face_and_first_perimeter_auto_increment: float
    absolute_spacing_between_support_face_and_first_perimeter_auto_maximum: float
    absolute_spacing_between_support_face_and_first_perimeter_auto_minimum: float
    absolute_spacing_between_support_face_and_first_perimeter_auto_priority: int
    absolute_spacing_between_support_face_and_first_perimeter_calculated: float
    absolute_spacing_between_perimeters_auto_increment: float
    absolute_spacing_between_perimeters_auto_maximum: float
    absolute_spacing_between_perimeters_auto_minimum: float
    absolute_spacing_between_perimeters_auto_priority: int
    absolute_spacing_between_perimeters_calculated: float
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[PunchingReinforcementType, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., nodes: _Optional[_Iterable[int]] = ..., material: _Optional[int] = ..., placement_type: _Optional[_Union[PunchingReinforcementPlacementType, str]] = ..., number_of_perimeters: _Optional[int] = ..., number_of_perimeters_auto_enabled: bool = ..., number_of_legs_in_each_perimeter: _Optional[int] = ..., number_of_legs_in_each_perimeter_auto_enabled: bool = ..., perimeter_spacing_type: _Optional[_Union[PunchingReinforcementPerimeterSpacingType, str]] = ..., multiple_static_depth_spacing_between_support_face_and_first_perimeter: _Optional[float] = ..., multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_enabled: bool = ..., multiple_static_depth_spacing_between_perimeters: _Optional[float] = ..., multiple_static_depth_spacing_between_perimeters_auto_enabled: bool = ..., absolute_spacing_between_support_face_and_first_perimeter: _Optional[float] = ..., absolute_spacing_between_support_face_and_first_perimeter_auto_enabled: bool = ..., absolute_spacing_between_perimeters: _Optional[float] = ..., absolute_spacing_between_perimeters_auto_enabled: bool = ..., bend_up_diameter: _Optional[float] = ..., bend_up_diameter_auto_enabled: bool = ..., perimeter_area: _Optional[float] = ..., total_area: _Optional[float] = ..., integrated_in_surfaces: _Optional[_Iterable[int]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., number_of_perimeters_auto_maximum: _Optional[int] = ..., number_of_perimeters_auto_minimum: _Optional[int] = ..., number_of_perimeters_auto_priority: _Optional[int] = ..., number_of_perimeters_calculated: _Optional[int] = ..., number_of_legs_in_each_perimeter_auto_maximum: _Optional[int] = ..., number_of_legs_in_each_perimeter_auto_minimum: _Optional[int] = ..., number_of_legs_in_each_perimeter_auto_priority: _Optional[int] = ..., number_of_legs_in_each_perimeter_calculated: _Optional[int] = ..., multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_increment: _Optional[float] = ..., multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_maximum: _Optional[float] = ..., multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_minimum: _Optional[float] = ..., multiple_static_depth_spacing_between_support_face_and_first_perimeter_auto_priority: _Optional[int] = ..., multiple_static_depth_spacing_between_support_face_and_first_perimeter_calculated: _Optional[float] = ..., multiple_static_depth_spacing_between_perimeters_auto_increment: _Optional[float] = ..., multiple_static_depth_spacing_between_perimeters_auto_maximum: _Optional[float] = ..., multiple_static_depth_spacing_between_perimeters_auto_minimum: _Optional[float] = ..., multiple_static_depth_spacing_between_perimeters_auto_priority: _Optional[int] = ..., multiple_static_depth_spacing_between_perimeters_calculated: _Optional[float] = ..., different_placement_perimeters: _Optional[_Union[PunchingReinforcementDifferentPlacementPerimetersTable, _Mapping]] = ..., different_placement_perimeter_spacing_type: _Optional[_Union[PunchingReinforcementDifferentPlacementPerimeterSpacingType, str]] = ..., bend_up_diameter_auto_maximum: _Optional[float] = ..., bend_up_diameter_auto_minimum: _Optional[float] = ..., bend_up_diameter_auto_priority: _Optional[int] = ..., bend_up_diameter_calculated: _Optional[float] = ..., bend_up_size_designation: _Optional[_Union[PunchingReinforcementBendUpSizeDesignation, str]] = ..., bend_up_size_designation_auto_maximum: _Optional[_Union[PunchingReinforcementBendUpSizeDesignationAutoMaximum, str]] = ..., bend_up_size_designation_auto_minimum: _Optional[_Union[PunchingReinforcementBendUpSizeDesignationAutoMinimum, str]] = ..., bend_up_diameter_auto_diameters_list: _Optional[_Iterable[int]] = ..., bend_up_diameter_auto_diameters_list_enabled: bool = ..., absolute_spacing_between_support_face_and_first_perimeter_auto_increment: _Optional[float] = ..., absolute_spacing_between_support_face_and_first_perimeter_auto_maximum: _Optional[float] = ..., absolute_spacing_between_support_face_and_first_perimeter_auto_minimum: _Optional[float] = ..., absolute_spacing_between_support_face_and_first_perimeter_auto_priority: _Optional[int] = ..., absolute_spacing_between_support_face_and_first_perimeter_calculated: _Optional[float] = ..., absolute_spacing_between_perimeters_auto_increment: _Optional[float] = ..., absolute_spacing_between_perimeters_auto_maximum: _Optional[float] = ..., absolute_spacing_between_perimeters_auto_minimum: _Optional[float] = ..., absolute_spacing_between_perimeters_auto_priority: _Optional[int] = ..., absolute_spacing_between_perimeters_calculated: _Optional[float] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class PunchingReinforcementDifferentPlacementPerimetersTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[PunchingReinforcementDifferentPlacementPerimetersRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[PunchingReinforcementDifferentPlacementPerimetersRow, _Mapping]]] = ...) -> None: ...

class PunchingReinforcementDifferentPlacementPerimetersRow(_message.Message):
    __slots__ = ("no", "description", "number_links_count", "spacing", "reinforcement_area")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NUMBER_LINKS_COUNT_FIELD_NUMBER: _ClassVar[int]
    SPACING_FIELD_NUMBER: _ClassVar[int]
    REINFORCEMENT_AREA_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    number_links_count: int
    spacing: float
    reinforcement_area: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., number_links_count: _Optional[int] = ..., spacing: _Optional[float] = ..., reinforcement_area: _Optional[float] = ...) -> None: ...
