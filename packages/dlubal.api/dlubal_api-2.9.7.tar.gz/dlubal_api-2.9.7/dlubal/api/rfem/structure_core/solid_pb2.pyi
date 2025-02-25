from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SolidType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_TYPE_UNKNOWN: _ClassVar[SolidType]
    SOLID_TYPE_CONTACT: _ClassVar[SolidType]
    SOLID_TYPE_GAS: _ClassVar[SolidType]
    SOLID_TYPE_HOLE: _ClassVar[SolidType]
    SOLID_TYPE_INTERSECTION: _ClassVar[SolidType]
    SOLID_TYPE_SOIL: _ClassVar[SolidType]
    SOLID_TYPE_STANDARD: _ClassVar[SolidType]

class SolidNumberOfFiniteElementLayersInputType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_NUMBER_OF_FINITE_ELEMENT_LAYERS_INPUT_TYPE_USER_DEFINED: _ClassVar[SolidNumberOfFiniteElementLayersInputType]
    SOLID_NUMBER_OF_FINITE_ELEMENT_LAYERS_INPUT_TYPE_ACCORDING_TO_MESH_SETTINGS: _ClassVar[SolidNumberOfFiniteElementLayersInputType]

class SolidSpecificDirectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_SPECIFIC_DIRECTION_TYPE_ROTATED_VIA_3_ANGLES: _ClassVar[SolidSpecificDirectionType]
    SOLID_SPECIFIC_DIRECTION_TYPE_DIRECTED_TO_NODE: _ClassVar[SolidSpecificDirectionType]
    SOLID_SPECIFIC_DIRECTION_TYPE_PARALLEL_TO_CS_OF_LINE: _ClassVar[SolidSpecificDirectionType]
    SOLID_SPECIFIC_DIRECTION_TYPE_PARALLEL_TO_CS_OF_MEMBER: _ClassVar[SolidSpecificDirectionType]
    SOLID_SPECIFIC_DIRECTION_TYPE_PARALLEL_TO_TWO_NODES: _ClassVar[SolidSpecificDirectionType]

class SolidAxesSequence(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_AXES_SEQUENCE_XYZ: _ClassVar[SolidAxesSequence]
    SOLID_AXES_SEQUENCE_XZY: _ClassVar[SolidAxesSequence]
    SOLID_AXES_SEQUENCE_YXZ: _ClassVar[SolidAxesSequence]
    SOLID_AXES_SEQUENCE_YZX: _ClassVar[SolidAxesSequence]
    SOLID_AXES_SEQUENCE_ZXY: _ClassVar[SolidAxesSequence]
    SOLID_AXES_SEQUENCE_ZYX: _ClassVar[SolidAxesSequence]

class SolidDirectedToNodeFirstAxis(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_DIRECTED_TO_NODE_FIRST_AXIS_X: _ClassVar[SolidDirectedToNodeFirstAxis]
    SOLID_DIRECTED_TO_NODE_FIRST_AXIS_Y: _ClassVar[SolidDirectedToNodeFirstAxis]
    SOLID_DIRECTED_TO_NODE_FIRST_AXIS_Z: _ClassVar[SolidDirectedToNodeFirstAxis]

class SolidDirectedToNodeSecondAxis(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_DIRECTED_TO_NODE_SECOND_AXIS_X: _ClassVar[SolidDirectedToNodeSecondAxis]
    SOLID_DIRECTED_TO_NODE_SECOND_AXIS_Y: _ClassVar[SolidDirectedToNodeSecondAxis]
    SOLID_DIRECTED_TO_NODE_SECOND_AXIS_Z: _ClassVar[SolidDirectedToNodeSecondAxis]

class SolidParallelToTwoNodesFirstAxis(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_PARALLEL_TO_TWO_NODES_FIRST_AXIS_X: _ClassVar[SolidParallelToTwoNodesFirstAxis]
    SOLID_PARALLEL_TO_TWO_NODES_FIRST_AXIS_Y: _ClassVar[SolidParallelToTwoNodesFirstAxis]
    SOLID_PARALLEL_TO_TWO_NODES_FIRST_AXIS_Z: _ClassVar[SolidParallelToTwoNodesFirstAxis]

class SolidParallelToTwoNodesSecondAxis(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_PARALLEL_TO_TWO_NODES_SECOND_AXIS_X: _ClassVar[SolidParallelToTwoNodesSecondAxis]
    SOLID_PARALLEL_TO_TWO_NODES_SECOND_AXIS_Y: _ClassVar[SolidParallelToTwoNodesSecondAxis]
    SOLID_PARALLEL_TO_TWO_NODES_SECOND_AXIS_Z: _ClassVar[SolidParallelToTwoNodesSecondAxis]
SOLID_TYPE_UNKNOWN: SolidType
SOLID_TYPE_CONTACT: SolidType
SOLID_TYPE_GAS: SolidType
SOLID_TYPE_HOLE: SolidType
SOLID_TYPE_INTERSECTION: SolidType
SOLID_TYPE_SOIL: SolidType
SOLID_TYPE_STANDARD: SolidType
SOLID_NUMBER_OF_FINITE_ELEMENT_LAYERS_INPUT_TYPE_USER_DEFINED: SolidNumberOfFiniteElementLayersInputType
SOLID_NUMBER_OF_FINITE_ELEMENT_LAYERS_INPUT_TYPE_ACCORDING_TO_MESH_SETTINGS: SolidNumberOfFiniteElementLayersInputType
SOLID_SPECIFIC_DIRECTION_TYPE_ROTATED_VIA_3_ANGLES: SolidSpecificDirectionType
SOLID_SPECIFIC_DIRECTION_TYPE_DIRECTED_TO_NODE: SolidSpecificDirectionType
SOLID_SPECIFIC_DIRECTION_TYPE_PARALLEL_TO_CS_OF_LINE: SolidSpecificDirectionType
SOLID_SPECIFIC_DIRECTION_TYPE_PARALLEL_TO_CS_OF_MEMBER: SolidSpecificDirectionType
SOLID_SPECIFIC_DIRECTION_TYPE_PARALLEL_TO_TWO_NODES: SolidSpecificDirectionType
SOLID_AXES_SEQUENCE_XYZ: SolidAxesSequence
SOLID_AXES_SEQUENCE_XZY: SolidAxesSequence
SOLID_AXES_SEQUENCE_YXZ: SolidAxesSequence
SOLID_AXES_SEQUENCE_YZX: SolidAxesSequence
SOLID_AXES_SEQUENCE_ZXY: SolidAxesSequence
SOLID_AXES_SEQUENCE_ZYX: SolidAxesSequence
SOLID_DIRECTED_TO_NODE_FIRST_AXIS_X: SolidDirectedToNodeFirstAxis
SOLID_DIRECTED_TO_NODE_FIRST_AXIS_Y: SolidDirectedToNodeFirstAxis
SOLID_DIRECTED_TO_NODE_FIRST_AXIS_Z: SolidDirectedToNodeFirstAxis
SOLID_DIRECTED_TO_NODE_SECOND_AXIS_X: SolidDirectedToNodeSecondAxis
SOLID_DIRECTED_TO_NODE_SECOND_AXIS_Y: SolidDirectedToNodeSecondAxis
SOLID_DIRECTED_TO_NODE_SECOND_AXIS_Z: SolidDirectedToNodeSecondAxis
SOLID_PARALLEL_TO_TWO_NODES_FIRST_AXIS_X: SolidParallelToTwoNodesFirstAxis
SOLID_PARALLEL_TO_TWO_NODES_FIRST_AXIS_Y: SolidParallelToTwoNodesFirstAxis
SOLID_PARALLEL_TO_TWO_NODES_FIRST_AXIS_Z: SolidParallelToTwoNodesFirstAxis
SOLID_PARALLEL_TO_TWO_NODES_SECOND_AXIS_X: SolidParallelToTwoNodesSecondAxis
SOLID_PARALLEL_TO_TWO_NODES_SECOND_AXIS_Y: SolidParallelToTwoNodesSecondAxis
SOLID_PARALLEL_TO_TWO_NODES_SECOND_AXIS_Z: SolidParallelToTwoNodesSecondAxis

class Solid(_message.Message):
    __slots__ = ("no", "type", "analytical_center_of_gravity", "analytical_center_of_gravity_x", "analytical_center_of_gravity_y", "analytical_center_of_gravity_z", "analytical_mass", "analytical_surface_area", "analytical_volume", "boundary_surfaces", "center_of_gravity", "center_of_gravity_x", "center_of_gravity_y", "center_of_gravity_z", "gas", "is_deactivated_for_calculation", "mass", "material", "mesh_refinement", "solid_contact", "solid_contact_first_surface", "solid_contact_second_surface", "stress_analysis_configuration", "surface_area", "volume", "comment", "is_generated", "generating_object_info", "is_layered_mesh_enabled", "layered_mesh_first_surface", "layered_mesh_second_surface", "number_of_finite_element_layers_input_type", "number_of_finite_element_layers", "specific_direction_enabled", "coordinate_system", "specific_direction_type", "axes_sequence", "rotated_about_angle_x", "rotated_about_angle_y", "rotated_about_angle_z", "rotated_about_angle_1", "rotated_about_angle_2", "rotated_about_angle_3", "directed_to_node_direction_node", "directed_to_node_plane_node", "directed_to_node_first_axis", "directed_to_node_second_axis", "parallel_to_two_nodes_first_node", "parallel_to_two_nodes_second_node", "parallel_to_two_nodes_plane_node", "parallel_to_two_nodes_first_axis", "parallel_to_two_nodes_second_axis", "parallel_to_line", "parallel_to_member", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_CENTER_OF_GRAVITY_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_CENTER_OF_GRAVITY_X_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_CENTER_OF_GRAVITY_Y_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_CENTER_OF_GRAVITY_Z_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_MASS_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_SURFACE_AREA_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_VOLUME_FIELD_NUMBER: _ClassVar[int]
    BOUNDARY_SURFACES_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_X_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_Y_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_Z_FIELD_NUMBER: _ClassVar[int]
    GAS_FIELD_NUMBER: _ClassVar[int]
    IS_DEACTIVATED_FOR_CALCULATION_FIELD_NUMBER: _ClassVar[int]
    MASS_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_FIELD_NUMBER: _ClassVar[int]
    MESH_REFINEMENT_FIELD_NUMBER: _ClassVar[int]
    SOLID_CONTACT_FIELD_NUMBER: _ClassVar[int]
    SOLID_CONTACT_FIRST_SURFACE_FIELD_NUMBER: _ClassVar[int]
    SOLID_CONTACT_SECOND_SURFACE_FIELD_NUMBER: _ClassVar[int]
    STRESS_ANALYSIS_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SURFACE_AREA_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    IS_LAYERED_MESH_ENABLED_FIELD_NUMBER: _ClassVar[int]
    LAYERED_MESH_FIRST_SURFACE_FIELD_NUMBER: _ClassVar[int]
    LAYERED_MESH_SECOND_SURFACE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_FINITE_ELEMENT_LAYERS_INPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_FINITE_ELEMENT_LAYERS_FIELD_NUMBER: _ClassVar[int]
    SPECIFIC_DIRECTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    SPECIFIC_DIRECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    AXES_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    ROTATED_ABOUT_ANGLE_X_FIELD_NUMBER: _ClassVar[int]
    ROTATED_ABOUT_ANGLE_Y_FIELD_NUMBER: _ClassVar[int]
    ROTATED_ABOUT_ANGLE_Z_FIELD_NUMBER: _ClassVar[int]
    ROTATED_ABOUT_ANGLE_1_FIELD_NUMBER: _ClassVar[int]
    ROTATED_ABOUT_ANGLE_2_FIELD_NUMBER: _ClassVar[int]
    ROTATED_ABOUT_ANGLE_3_FIELD_NUMBER: _ClassVar[int]
    DIRECTED_TO_NODE_DIRECTION_NODE_FIELD_NUMBER: _ClassVar[int]
    DIRECTED_TO_NODE_PLANE_NODE_FIELD_NUMBER: _ClassVar[int]
    DIRECTED_TO_NODE_FIRST_AXIS_FIELD_NUMBER: _ClassVar[int]
    DIRECTED_TO_NODE_SECOND_AXIS_FIELD_NUMBER: _ClassVar[int]
    PARALLEL_TO_TWO_NODES_FIRST_NODE_FIELD_NUMBER: _ClassVar[int]
    PARALLEL_TO_TWO_NODES_SECOND_NODE_FIELD_NUMBER: _ClassVar[int]
    PARALLEL_TO_TWO_NODES_PLANE_NODE_FIELD_NUMBER: _ClassVar[int]
    PARALLEL_TO_TWO_NODES_FIRST_AXIS_FIELD_NUMBER: _ClassVar[int]
    PARALLEL_TO_TWO_NODES_SECOND_AXIS_FIELD_NUMBER: _ClassVar[int]
    PARALLEL_TO_LINE_FIELD_NUMBER: _ClassVar[int]
    PARALLEL_TO_MEMBER_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: SolidType
    analytical_center_of_gravity: _common_pb2.Vector3d
    analytical_center_of_gravity_x: float
    analytical_center_of_gravity_y: float
    analytical_center_of_gravity_z: float
    analytical_mass: float
    analytical_surface_area: float
    analytical_volume: float
    boundary_surfaces: _containers.RepeatedScalarFieldContainer[int]
    center_of_gravity: _common_pb2.Vector3d
    center_of_gravity_x: float
    center_of_gravity_y: float
    center_of_gravity_z: float
    gas: int
    is_deactivated_for_calculation: bool
    mass: float
    material: int
    mesh_refinement: int
    solid_contact: int
    solid_contact_first_surface: int
    solid_contact_second_surface: int
    stress_analysis_configuration: int
    surface_area: float
    volume: float
    comment: str
    is_generated: bool
    generating_object_info: str
    is_layered_mesh_enabled: bool
    layered_mesh_first_surface: int
    layered_mesh_second_surface: int
    number_of_finite_element_layers_input_type: SolidNumberOfFiniteElementLayersInputType
    number_of_finite_element_layers: int
    specific_direction_enabled: bool
    coordinate_system: int
    specific_direction_type: SolidSpecificDirectionType
    axes_sequence: SolidAxesSequence
    rotated_about_angle_x: float
    rotated_about_angle_y: float
    rotated_about_angle_z: float
    rotated_about_angle_1: float
    rotated_about_angle_2: float
    rotated_about_angle_3: float
    directed_to_node_direction_node: int
    directed_to_node_plane_node: int
    directed_to_node_first_axis: SolidDirectedToNodeFirstAxis
    directed_to_node_second_axis: SolidDirectedToNodeSecondAxis
    parallel_to_two_nodes_first_node: int
    parallel_to_two_nodes_second_node: int
    parallel_to_two_nodes_plane_node: int
    parallel_to_two_nodes_first_axis: SolidParallelToTwoNodesFirstAxis
    parallel_to_two_nodes_second_axis: SolidParallelToTwoNodesSecondAxis
    parallel_to_line: int
    parallel_to_member: int
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[SolidType, str]] = ..., analytical_center_of_gravity: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., analytical_center_of_gravity_x: _Optional[float] = ..., analytical_center_of_gravity_y: _Optional[float] = ..., analytical_center_of_gravity_z: _Optional[float] = ..., analytical_mass: _Optional[float] = ..., analytical_surface_area: _Optional[float] = ..., analytical_volume: _Optional[float] = ..., boundary_surfaces: _Optional[_Iterable[int]] = ..., center_of_gravity: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., center_of_gravity_x: _Optional[float] = ..., center_of_gravity_y: _Optional[float] = ..., center_of_gravity_z: _Optional[float] = ..., gas: _Optional[int] = ..., is_deactivated_for_calculation: bool = ..., mass: _Optional[float] = ..., material: _Optional[int] = ..., mesh_refinement: _Optional[int] = ..., solid_contact: _Optional[int] = ..., solid_contact_first_surface: _Optional[int] = ..., solid_contact_second_surface: _Optional[int] = ..., stress_analysis_configuration: _Optional[int] = ..., surface_area: _Optional[float] = ..., volume: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., is_layered_mesh_enabled: bool = ..., layered_mesh_first_surface: _Optional[int] = ..., layered_mesh_second_surface: _Optional[int] = ..., number_of_finite_element_layers_input_type: _Optional[_Union[SolidNumberOfFiniteElementLayersInputType, str]] = ..., number_of_finite_element_layers: _Optional[int] = ..., specific_direction_enabled: bool = ..., coordinate_system: _Optional[int] = ..., specific_direction_type: _Optional[_Union[SolidSpecificDirectionType, str]] = ..., axes_sequence: _Optional[_Union[SolidAxesSequence, str]] = ..., rotated_about_angle_x: _Optional[float] = ..., rotated_about_angle_y: _Optional[float] = ..., rotated_about_angle_z: _Optional[float] = ..., rotated_about_angle_1: _Optional[float] = ..., rotated_about_angle_2: _Optional[float] = ..., rotated_about_angle_3: _Optional[float] = ..., directed_to_node_direction_node: _Optional[int] = ..., directed_to_node_plane_node: _Optional[int] = ..., directed_to_node_first_axis: _Optional[_Union[SolidDirectedToNodeFirstAxis, str]] = ..., directed_to_node_second_axis: _Optional[_Union[SolidDirectedToNodeSecondAxis, str]] = ..., parallel_to_two_nodes_first_node: _Optional[int] = ..., parallel_to_two_nodes_second_node: _Optional[int] = ..., parallel_to_two_nodes_plane_node: _Optional[int] = ..., parallel_to_two_nodes_first_axis: _Optional[_Union[SolidParallelToTwoNodesFirstAxis, str]] = ..., parallel_to_two_nodes_second_axis: _Optional[_Union[SolidParallelToTwoNodesSecondAxis, str]] = ..., parallel_to_line: _Optional[int] = ..., parallel_to_member: _Optional[int] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
