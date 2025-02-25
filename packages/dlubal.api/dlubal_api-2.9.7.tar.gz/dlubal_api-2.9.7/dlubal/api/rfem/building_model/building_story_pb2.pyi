from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BuildingStoryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUILDING_STORY_TYPE_UNKNOWN: _ClassVar[BuildingStoryType]
    BUILDING_STORY_TYPE_STANDARD: _ClassVar[BuildingStoryType]

class BuildingStoryModifyGeometryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUILDING_STORY_MODIFY_GEOMETRY_TYPE_DO_NOTHING: _ClassVar[BuildingStoryModifyGeometryType]
    BUILDING_STORY_MODIFY_GEOMETRY_TYPE_CONST_FROM_STORY_GROUND: _ClassVar[BuildingStoryModifyGeometryType]
    BUILDING_STORY_MODIFY_GEOMETRY_TYPE_CONST_FROM_STORY_ROOF: _ClassVar[BuildingStoryModifyGeometryType]
    BUILDING_STORY_MODIFY_GEOMETRY_TYPE_PROPORTIONAL: _ClassVar[BuildingStoryModifyGeometryType]

class BuildingStoryThicknessType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUILDING_STORY_THICKNESS_TYPE_EFFECTIVE_HEIGHT: _ClassVar[BuildingStoryThicknessType]
    BUILDING_STORY_THICKNESS_TYPE_CLEAR_HEIGHT: _ClassVar[BuildingStoryThicknessType]

class BuildingStorySlabStiffnessType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUILDING_STORY_SLAB_STIFFNESS_TYPE_STANDARD: _ClassVar[BuildingStorySlabStiffnessType]
    BUILDING_STORY_SLAB_STIFFNESS_TYPE_RIGID_DIAPHRAGM: _ClassVar[BuildingStorySlabStiffnessType]

class BuildingStoryFloorStiffnessType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUILDING_STORY_FLOOR_STIFFNESS_TYPE_STANDARD: _ClassVar[BuildingStoryFloorStiffnessType]
    BUILDING_STORY_FLOOR_STIFFNESS_TYPE_FLEXIBLE_DIAPHRAGM: _ClassVar[BuildingStoryFloorStiffnessType]
    BUILDING_STORY_FLOOR_STIFFNESS_TYPE_RIGID_DIAPHRAGM: _ClassVar[BuildingStoryFloorStiffnessType]
    BUILDING_STORY_FLOOR_STIFFNESS_TYPE_SEMIRIGID: _ClassVar[BuildingStoryFloorStiffnessType]

class BuildingStoryLineSupportModel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUILDING_STORY_LINE_SUPPORT_MODEL_HINGED: _ClassVar[BuildingStoryLineSupportModel]
    BUILDING_STORY_LINE_SUPPORT_MODEL_HINGE_HINGE: _ClassVar[BuildingStoryLineSupportModel]
    BUILDING_STORY_LINE_SUPPORT_MODEL_HINGE_RIGID: _ClassVar[BuildingStoryLineSupportModel]
    BUILDING_STORY_LINE_SUPPORT_MODEL_RIGID_HINGE: _ClassVar[BuildingStoryLineSupportModel]
    BUILDING_STORY_LINE_SUPPORT_MODEL_RIGID_RIGID: _ClassVar[BuildingStoryLineSupportModel]

class BuildingStoryNodalSupportModel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUILDING_STORY_NODAL_SUPPORT_MODEL_HINGED: _ClassVar[BuildingStoryNodalSupportModel]
    BUILDING_STORY_NODAL_SUPPORT_MODEL_ACCORDING_TO_MEMBER_TYPE: _ClassVar[BuildingStoryNodalSupportModel]
    BUILDING_STORY_NODAL_SUPPORT_MODEL_HINGE_HINGE: _ClassVar[BuildingStoryNodalSupportModel]
    BUILDING_STORY_NODAL_SUPPORT_MODEL_HINGE_RIGID: _ClassVar[BuildingStoryNodalSupportModel]
    BUILDING_STORY_NODAL_SUPPORT_MODEL_RIGID_HINGE: _ClassVar[BuildingStoryNodalSupportModel]
    BUILDING_STORY_NODAL_SUPPORT_MODEL_RIGID_RIGID: _ClassVar[BuildingStoryNodalSupportModel]
BUILDING_STORY_TYPE_UNKNOWN: BuildingStoryType
BUILDING_STORY_TYPE_STANDARD: BuildingStoryType
BUILDING_STORY_MODIFY_GEOMETRY_TYPE_DO_NOTHING: BuildingStoryModifyGeometryType
BUILDING_STORY_MODIFY_GEOMETRY_TYPE_CONST_FROM_STORY_GROUND: BuildingStoryModifyGeometryType
BUILDING_STORY_MODIFY_GEOMETRY_TYPE_CONST_FROM_STORY_ROOF: BuildingStoryModifyGeometryType
BUILDING_STORY_MODIFY_GEOMETRY_TYPE_PROPORTIONAL: BuildingStoryModifyGeometryType
BUILDING_STORY_THICKNESS_TYPE_EFFECTIVE_HEIGHT: BuildingStoryThicknessType
BUILDING_STORY_THICKNESS_TYPE_CLEAR_HEIGHT: BuildingStoryThicknessType
BUILDING_STORY_SLAB_STIFFNESS_TYPE_STANDARD: BuildingStorySlabStiffnessType
BUILDING_STORY_SLAB_STIFFNESS_TYPE_RIGID_DIAPHRAGM: BuildingStorySlabStiffnessType
BUILDING_STORY_FLOOR_STIFFNESS_TYPE_STANDARD: BuildingStoryFloorStiffnessType
BUILDING_STORY_FLOOR_STIFFNESS_TYPE_FLEXIBLE_DIAPHRAGM: BuildingStoryFloorStiffnessType
BUILDING_STORY_FLOOR_STIFFNESS_TYPE_RIGID_DIAPHRAGM: BuildingStoryFloorStiffnessType
BUILDING_STORY_FLOOR_STIFFNESS_TYPE_SEMIRIGID: BuildingStoryFloorStiffnessType
BUILDING_STORY_LINE_SUPPORT_MODEL_HINGED: BuildingStoryLineSupportModel
BUILDING_STORY_LINE_SUPPORT_MODEL_HINGE_HINGE: BuildingStoryLineSupportModel
BUILDING_STORY_LINE_SUPPORT_MODEL_HINGE_RIGID: BuildingStoryLineSupportModel
BUILDING_STORY_LINE_SUPPORT_MODEL_RIGID_HINGE: BuildingStoryLineSupportModel
BUILDING_STORY_LINE_SUPPORT_MODEL_RIGID_RIGID: BuildingStoryLineSupportModel
BUILDING_STORY_NODAL_SUPPORT_MODEL_HINGED: BuildingStoryNodalSupportModel
BUILDING_STORY_NODAL_SUPPORT_MODEL_ACCORDING_TO_MEMBER_TYPE: BuildingStoryNodalSupportModel
BUILDING_STORY_NODAL_SUPPORT_MODEL_HINGE_HINGE: BuildingStoryNodalSupportModel
BUILDING_STORY_NODAL_SUPPORT_MODEL_HINGE_RIGID: BuildingStoryNodalSupportModel
BUILDING_STORY_NODAL_SUPPORT_MODEL_RIGID_HINGE: BuildingStoryNodalSupportModel
BUILDING_STORY_NODAL_SUPPORT_MODEL_RIGID_RIGID: BuildingStoryNodalSupportModel

class BuildingStory(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "story_no", "elevation", "bottom_elevation", "height", "modified_height", "thickness", "info", "comment", "total_info", "modify_geometry_type", "thickness_type", "slab_stiffness_type", "floor_stiffness_type", "vertical_result_line_active", "vertical_result_line_position_x", "vertical_result_line_position_y", "vertical_result_line_relative", "vertical_result_line_relative_position_x", "vertical_result_line_relative_position_y", "mass", "center_of_gravity_x", "center_of_gravity_y", "line_support_model", "nodal_support_model", "building_stories_zero_value", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STORY_NO_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_ELEVATION_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_INFO_FIELD_NUMBER: _ClassVar[int]
    MODIFY_GEOMETRY_TYPE_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_TYPE_FIELD_NUMBER: _ClassVar[int]
    SLAB_STIFFNESS_TYPE_FIELD_NUMBER: _ClassVar[int]
    FLOOR_STIFFNESS_TYPE_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_RESULT_LINE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_RESULT_LINE_POSITION_X_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_RESULT_LINE_POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_RESULT_LINE_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_RESULT_LINE_RELATIVE_POSITION_X_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_RESULT_LINE_RELATIVE_POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    MASS_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_X_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_Y_FIELD_NUMBER: _ClassVar[int]
    LINE_SUPPORT_MODEL_FIELD_NUMBER: _ClassVar[int]
    NODAL_SUPPORT_MODEL_FIELD_NUMBER: _ClassVar[int]
    BUILDING_STORIES_ZERO_VALUE_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: BuildingStoryType
    user_defined_name_enabled: bool
    name: str
    story_no: int
    elevation: float
    bottom_elevation: float
    height: float
    modified_height: float
    thickness: float
    info: BuildingStoryInfoAndChildItemsTable
    comment: str
    total_info: BuildingStoryTotalInfoAndChildItemsTable
    modify_geometry_type: BuildingStoryModifyGeometryType
    thickness_type: BuildingStoryThicknessType
    slab_stiffness_type: BuildingStorySlabStiffnessType
    floor_stiffness_type: BuildingStoryFloorStiffnessType
    vertical_result_line_active: bool
    vertical_result_line_position_x: float
    vertical_result_line_position_y: float
    vertical_result_line_relative: bool
    vertical_result_line_relative_position_x: float
    vertical_result_line_relative_position_y: float
    mass: float
    center_of_gravity_x: float
    center_of_gravity_y: float
    line_support_model: BuildingStoryLineSupportModel
    nodal_support_model: BuildingStoryNodalSupportModel
    building_stories_zero_value: float
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[BuildingStoryType, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., story_no: _Optional[int] = ..., elevation: _Optional[float] = ..., bottom_elevation: _Optional[float] = ..., height: _Optional[float] = ..., modified_height: _Optional[float] = ..., thickness: _Optional[float] = ..., info: _Optional[_Union[BuildingStoryInfoAndChildItemsTable, _Mapping]] = ..., comment: _Optional[str] = ..., total_info: _Optional[_Union[BuildingStoryTotalInfoAndChildItemsTable, _Mapping]] = ..., modify_geometry_type: _Optional[_Union[BuildingStoryModifyGeometryType, str]] = ..., thickness_type: _Optional[_Union[BuildingStoryThicknessType, str]] = ..., slab_stiffness_type: _Optional[_Union[BuildingStorySlabStiffnessType, str]] = ..., floor_stiffness_type: _Optional[_Union[BuildingStoryFloorStiffnessType, str]] = ..., vertical_result_line_active: bool = ..., vertical_result_line_position_x: _Optional[float] = ..., vertical_result_line_position_y: _Optional[float] = ..., vertical_result_line_relative: bool = ..., vertical_result_line_relative_position_x: _Optional[float] = ..., vertical_result_line_relative_position_y: _Optional[float] = ..., mass: _Optional[float] = ..., center_of_gravity_x: _Optional[float] = ..., center_of_gravity_y: _Optional[float] = ..., line_support_model: _Optional[_Union[BuildingStoryLineSupportModel, str]] = ..., nodal_support_model: _Optional[_Union[BuildingStoryNodalSupportModel, str]] = ..., building_stories_zero_value: _Optional[float] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class BuildingStoryInfoAndChildItemsTable(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class BuildingStoryTotalInfoAndChildItemsTable(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
