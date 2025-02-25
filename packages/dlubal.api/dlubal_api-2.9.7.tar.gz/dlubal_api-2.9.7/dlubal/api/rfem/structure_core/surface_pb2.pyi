from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SurfaceGeometry(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_GEOMETRY_UNKNOWN: _ClassVar[SurfaceGeometry]
    SURFACE_GEOMETRY_MINIMUM_CURVATURE_SPLINE: _ClassVar[SurfaceGeometry]
    SURFACE_GEOMETRY_NURBS: _ClassVar[SurfaceGeometry]
    SURFACE_GEOMETRY_PIPE: _ClassVar[SurfaceGeometry]
    SURFACE_GEOMETRY_PLANE: _ClassVar[SurfaceGeometry]
    SURFACE_GEOMETRY_QUADRANGLE: _ClassVar[SurfaceGeometry]
    SURFACE_GEOMETRY_ROTATED: _ClassVar[SurfaceGeometry]
    SURFACE_GEOMETRY_TRIMMED: _ClassVar[SurfaceGeometry]

class SurfaceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_TYPE_STANDARD: _ClassVar[SurfaceType]
    SURFACE_TYPE_FLOOR: _ClassVar[SurfaceType]
    SURFACE_TYPE_FLOOR_DIAPHRAGM: _ClassVar[SurfaceType]
    SURFACE_TYPE_FLOOR_FLEXIBLE_DIAPHRAGM: _ClassVar[SurfaceType]
    SURFACE_TYPE_FLOOR_SEMIRIGID: _ClassVar[SurfaceType]
    SURFACE_TYPE_GROUNDWATER: _ClassVar[SurfaceType]
    SURFACE_TYPE_LOAD_TRANSFER: _ClassVar[SurfaceType]
    SURFACE_TYPE_MEMBRANE: _ClassVar[SurfaceType]
    SURFACE_TYPE_RIGID: _ClassVar[SurfaceType]
    SURFACE_TYPE_WITHOUT_MEMBRANE_TENSION: _ClassVar[SurfaceType]
    SURFACE_TYPE_WITHOUT_THICKNESS: _ClassVar[SurfaceType]

class SurfaceLoadTransferDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_LOAD_TRANSFER_DIRECTION_IN_X: _ClassVar[SurfaceLoadTransferDirection]
    SURFACE_LOAD_TRANSFER_DIRECTION_IN_BOTH: _ClassVar[SurfaceLoadTransferDirection]
    SURFACE_LOAD_TRANSFER_DIRECTION_IN_Y: _ClassVar[SurfaceLoadTransferDirection]
    SURFACE_LOAD_TRANSFER_DIRECTION_ISOTROPIC: _ClassVar[SurfaceLoadTransferDirection]

class SurfaceLoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_LOAD_DISTRIBUTION_UNIFORM: _ClassVar[SurfaceLoadDistribution]
    SURFACE_LOAD_DISTRIBUTION_VARYING_LINEAR: _ClassVar[SurfaceLoadDistribution]

class SurfaceQuadranglePreferableShape(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_QUADRANGLE_PREFERABLE_SHAPE_ROTATED: _ClassVar[SurfaceQuadranglePreferableShape]
    SURFACE_QUADRANGLE_PREFERABLE_SHAPE_PIPE: _ClassVar[SurfaceQuadranglePreferableShape]

class SurfaceMeshingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_MESHING_TYPE_USE_GLOBAL_SETTINGS: _ClassVar[SurfaceMeshingType]
    SURFACE_MESHING_TYPE_FREE: _ClassVar[SurfaceMeshingType]
    SURFACE_MESHING_TYPE_MAPPED: _ClassVar[SurfaceMeshingType]

class SurfaceInputAxesRotationSpecificationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_INPUT_AXES_ROTATION_SPECIFICATION_TYPE_ANGULAR_ROTATION: _ClassVar[SurfaceInputAxesRotationSpecificationType]
    SURFACE_INPUT_AXES_ROTATION_SPECIFICATION_TYPE_DIRECT_TO_POINT: _ClassVar[SurfaceInputAxesRotationSpecificationType]
    SURFACE_INPUT_AXES_ROTATION_SPECIFICATION_TYPE_PARALLEL_TO_COORDINATE_SYSTEM: _ClassVar[SurfaceInputAxesRotationSpecificationType]
    SURFACE_INPUT_AXES_ROTATION_SPECIFICATION_TYPE_PARALLEL_TO_LINES: _ClassVar[SurfaceInputAxesRotationSpecificationType]

class SurfaceInputAxesAxis(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_INPUT_AXES_AXIS_X: _ClassVar[SurfaceInputAxesAxis]
    SURFACE_INPUT_AXES_AXIS_Y: _ClassVar[SurfaceInputAxesAxis]

class SurfaceResultAxesRotationSpecificationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_RESULT_AXES_ROTATION_SPECIFICATION_TYPE_IDENTICAL_TO_INPUT_AXES: _ClassVar[SurfaceResultAxesRotationSpecificationType]

class SurfaceGridType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_GRID_TYPE_CARTESIAN: _ClassVar[SurfaceGridType]
    SURFACE_GRID_TYPE_POLAR: _ClassVar[SurfaceGridType]

class SurfaceDeflectionCheckSurfaceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_DEFLECTION_CHECK_SURFACE_TYPE_DOUBLE_SUPPORTED: _ClassVar[SurfaceDeflectionCheckSurfaceType]
    SURFACE_DEFLECTION_CHECK_SURFACE_TYPE_CANTILEVER: _ClassVar[SurfaceDeflectionCheckSurfaceType]

class SurfaceDeflectionCheckDisplacementReference(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_DEFLECTION_CHECK_DISPLACEMENT_REFERENCE_DEFORMED_USER_DEFINED_REFERENCE_PLANE: _ClassVar[SurfaceDeflectionCheckDisplacementReference]
    SURFACE_DEFLECTION_CHECK_DISPLACEMENT_REFERENCE_PARALLEL_SURFACE: _ClassVar[SurfaceDeflectionCheckDisplacementReference]
    SURFACE_DEFLECTION_CHECK_DISPLACEMENT_REFERENCE_UNDEFORMED_SYSTEM: _ClassVar[SurfaceDeflectionCheckDisplacementReference]

class SurfaceDeflectionCheckReferenceLengthZDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_DEFLECTION_CHECK_REFERENCE_LENGTH_Z_DEFINITION_TYPE_MANUALLY: _ClassVar[SurfaceDeflectionCheckReferenceLengthZDefinitionType]
    SURFACE_DEFLECTION_CHECK_REFERENCE_LENGTH_Z_DEFINITION_TYPE_BY_MAXIMUM_BOUNDARY_LINE: _ClassVar[SurfaceDeflectionCheckReferenceLengthZDefinitionType]
    SURFACE_DEFLECTION_CHECK_REFERENCE_LENGTH_Z_DEFINITION_TYPE_BY_MINIMUM_BOUNDARY_LINE: _ClassVar[SurfaceDeflectionCheckReferenceLengthZDefinitionType]
SURFACE_GEOMETRY_UNKNOWN: SurfaceGeometry
SURFACE_GEOMETRY_MINIMUM_CURVATURE_SPLINE: SurfaceGeometry
SURFACE_GEOMETRY_NURBS: SurfaceGeometry
SURFACE_GEOMETRY_PIPE: SurfaceGeometry
SURFACE_GEOMETRY_PLANE: SurfaceGeometry
SURFACE_GEOMETRY_QUADRANGLE: SurfaceGeometry
SURFACE_GEOMETRY_ROTATED: SurfaceGeometry
SURFACE_GEOMETRY_TRIMMED: SurfaceGeometry
SURFACE_TYPE_STANDARD: SurfaceType
SURFACE_TYPE_FLOOR: SurfaceType
SURFACE_TYPE_FLOOR_DIAPHRAGM: SurfaceType
SURFACE_TYPE_FLOOR_FLEXIBLE_DIAPHRAGM: SurfaceType
SURFACE_TYPE_FLOOR_SEMIRIGID: SurfaceType
SURFACE_TYPE_GROUNDWATER: SurfaceType
SURFACE_TYPE_LOAD_TRANSFER: SurfaceType
SURFACE_TYPE_MEMBRANE: SurfaceType
SURFACE_TYPE_RIGID: SurfaceType
SURFACE_TYPE_WITHOUT_MEMBRANE_TENSION: SurfaceType
SURFACE_TYPE_WITHOUT_THICKNESS: SurfaceType
SURFACE_LOAD_TRANSFER_DIRECTION_IN_X: SurfaceLoadTransferDirection
SURFACE_LOAD_TRANSFER_DIRECTION_IN_BOTH: SurfaceLoadTransferDirection
SURFACE_LOAD_TRANSFER_DIRECTION_IN_Y: SurfaceLoadTransferDirection
SURFACE_LOAD_TRANSFER_DIRECTION_ISOTROPIC: SurfaceLoadTransferDirection
SURFACE_LOAD_DISTRIBUTION_UNIFORM: SurfaceLoadDistribution
SURFACE_LOAD_DISTRIBUTION_VARYING_LINEAR: SurfaceLoadDistribution
SURFACE_QUADRANGLE_PREFERABLE_SHAPE_ROTATED: SurfaceQuadranglePreferableShape
SURFACE_QUADRANGLE_PREFERABLE_SHAPE_PIPE: SurfaceQuadranglePreferableShape
SURFACE_MESHING_TYPE_USE_GLOBAL_SETTINGS: SurfaceMeshingType
SURFACE_MESHING_TYPE_FREE: SurfaceMeshingType
SURFACE_MESHING_TYPE_MAPPED: SurfaceMeshingType
SURFACE_INPUT_AXES_ROTATION_SPECIFICATION_TYPE_ANGULAR_ROTATION: SurfaceInputAxesRotationSpecificationType
SURFACE_INPUT_AXES_ROTATION_SPECIFICATION_TYPE_DIRECT_TO_POINT: SurfaceInputAxesRotationSpecificationType
SURFACE_INPUT_AXES_ROTATION_SPECIFICATION_TYPE_PARALLEL_TO_COORDINATE_SYSTEM: SurfaceInputAxesRotationSpecificationType
SURFACE_INPUT_AXES_ROTATION_SPECIFICATION_TYPE_PARALLEL_TO_LINES: SurfaceInputAxesRotationSpecificationType
SURFACE_INPUT_AXES_AXIS_X: SurfaceInputAxesAxis
SURFACE_INPUT_AXES_AXIS_Y: SurfaceInputAxesAxis
SURFACE_RESULT_AXES_ROTATION_SPECIFICATION_TYPE_IDENTICAL_TO_INPUT_AXES: SurfaceResultAxesRotationSpecificationType
SURFACE_GRID_TYPE_CARTESIAN: SurfaceGridType
SURFACE_GRID_TYPE_POLAR: SurfaceGridType
SURFACE_DEFLECTION_CHECK_SURFACE_TYPE_DOUBLE_SUPPORTED: SurfaceDeflectionCheckSurfaceType
SURFACE_DEFLECTION_CHECK_SURFACE_TYPE_CANTILEVER: SurfaceDeflectionCheckSurfaceType
SURFACE_DEFLECTION_CHECK_DISPLACEMENT_REFERENCE_DEFORMED_USER_DEFINED_REFERENCE_PLANE: SurfaceDeflectionCheckDisplacementReference
SURFACE_DEFLECTION_CHECK_DISPLACEMENT_REFERENCE_PARALLEL_SURFACE: SurfaceDeflectionCheckDisplacementReference
SURFACE_DEFLECTION_CHECK_DISPLACEMENT_REFERENCE_UNDEFORMED_SYSTEM: SurfaceDeflectionCheckDisplacementReference
SURFACE_DEFLECTION_CHECK_REFERENCE_LENGTH_Z_DEFINITION_TYPE_MANUALLY: SurfaceDeflectionCheckReferenceLengthZDefinitionType
SURFACE_DEFLECTION_CHECK_REFERENCE_LENGTH_Z_DEFINITION_TYPE_BY_MAXIMUM_BOUNDARY_LINE: SurfaceDeflectionCheckReferenceLengthZDefinitionType
SURFACE_DEFLECTION_CHECK_REFERENCE_LENGTH_Z_DEFINITION_TYPE_BY_MINIMUM_BOUNDARY_LINE: SurfaceDeflectionCheckReferenceLengthZDefinitionType

class Surface(_message.Message):
    __slots__ = ("no", "geometry", "type", "boundary_lines", "thickness", "material", "analytical_area", "analytical_volume", "analytical_mass", "analytical_center_of_gravity", "analytical_center_of_gravity_x", "analytical_center_of_gravity_y", "analytical_center_of_gravity_z", "area", "volume", "mass", "center_of_gravity", "center_of_gravity_x", "center_of_gravity_y", "center_of_gravity_z", "position", "position_short", "grid_enabled", "is_deactivated_for_calculation", "comment", "design_properties_via_surface", "design_properties_via_parent_surface_set", "design_properties_parent_surface_set", "load_transfer_direction", "is_surface_weight_enabled", "is_advanced_distribution_settings_enabled", "surface_weight", "sampling_factor", "stripe_width", "consider_member_eccentricity", "consider_section_distribution", "load_distribution", "neglect_equilibrium_of_moments", "excluded_members", "excluded_parallel_to_members", "excluded_lines", "excluded_parallel_to_lines", "excluded_nodes", "loaded_members", "loaded_lines", "loaded_nodes", "nurbs_control_point_count_in_direction_u", "nurbs_control_point_count_in_direction_v", "nurbs_order_in_direction_u", "nurbs_order_in_direction_v", "nurbs_control_points", "quadrangle_corner_nodes", "quadrangle_corner_node_1", "quadrangle_corner_node_2", "quadrangle_corner_node_3", "quadrangle_corner_node_4", "quadrangle_preferable_shape", "pipe_radius", "pipe_use_radius_end", "pipe_radius_end", "pipe_center_line", "pipe_generated_lines", "has_line_hinges", "support", "eccentricity", "mesh_refinement", "meshing_type", "input_axes_rotation_specification_type", "input_axes_angular_rotation", "input_axes_axis", "input_axes_lines", "input_axes_point_1", "input_axes_point_1_x", "input_axes_point_1_y", "input_axes_point_1_z", "input_axes_point_2", "input_axes_point_2_x", "input_axes_point_2_y", "input_axes_point_2_z", "input_axes_coordinate_system", "result_axes_rotation_specification_type", "reversed_normal", "grid_type", "grid_origin", "grid_origin_x", "grid_origin_y", "grid_origin_z", "grid_adapt_automatically", "grid_point_count_negative_x", "grid_point_count_positive_x", "grid_point_count_negative_y", "grid_point_count_positive_y", "grid_numbering_increment", "grid_point_count_r", "grid_distance_x", "grid_distance_y", "grid_distance_r", "grid_rotation_alpha", "grid_rotation_beta", "grid_angle_gamma", "auto_detection_of_integrated_objects", "integrated_nodes", "integrated_lines", "integrated_openings", "has_integrated_objects", "has_input_axes_rotation", "has_result_axes_rotation", "surface_timber_design_uls_configuration", "surface_timber_design_sls_configuration", "surface_timber_design_fr_configuration", "timber_service_class", "timber_moisture_class", "timber_service_conditions", "surface_reinforcements", "is_user_defined_concrete_cover_enabled", "concrete_cover_top", "concrete_cover_bottom", "user_defined_concrete_cover_top", "user_defined_concrete_cover_bottom", "concrete_durability_top", "concrete_durability_bottom", "reinforcement_direction_top", "reinforcement_direction_bottom", "deflection_check_surface_type", "deflection_check_displacement_reference", "deflection_check_reference_length_z", "deflection_check_reference_length_z_definition_type", "deflection_check_reference_plane_point_1", "deflection_check_reference_plane_point_1_x", "deflection_check_reference_plane_point_1_y", "deflection_check_reference_plane_point_1_z", "deflection_check_reference_plane_point_2", "deflection_check_reference_plane_point_2_x", "deflection_check_reference_plane_point_2_y", "deflection_check_reference_plane_point_2_z", "deflection_check_reference_plane_point_3", "deflection_check_reference_plane_point_3_x", "deflection_check_reference_plane_point_3_y", "deflection_check_reference_plane_point_3_z", "surface_reinforcement_table", "surface_concrete_design_uls_configuration", "surface_concrete_design_sls_configuration", "surface_concrete_design_fr_configuration", "surface_concrete_design_seismic_configuration", "rotated_boundary_line", "rotated_angle_of_rotation", "rotated_point_p", "rotated_point_p_x", "rotated_point_p_y", "rotated_point_p_z", "rotated_point_r", "rotated_point_r_x", "rotated_point_r_y", "rotated_point_r_z", "rotated_generated_lines", "stress_analysis_configuration", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    GEOMETRY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BOUNDARY_LINES_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_AREA_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_VOLUME_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_MASS_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_CENTER_OF_GRAVITY_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_CENTER_OF_GRAVITY_X_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_CENTER_OF_GRAVITY_Y_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_CENTER_OF_GRAVITY_Z_FIELD_NUMBER: _ClassVar[int]
    AREA_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    MASS_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_X_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_Y_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_Z_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    POSITION_SHORT_FIELD_NUMBER: _ClassVar[int]
    GRID_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IS_DEACTIVATED_FOR_CALCULATION_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    DESIGN_PROPERTIES_VIA_SURFACE_FIELD_NUMBER: _ClassVar[int]
    DESIGN_PROPERTIES_VIA_PARENT_SURFACE_SET_FIELD_NUMBER: _ClassVar[int]
    DESIGN_PROPERTIES_PARENT_SURFACE_SET_FIELD_NUMBER: _ClassVar[int]
    LOAD_TRANSFER_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    IS_SURFACE_WEIGHT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IS_ADVANCED_DISTRIBUTION_SETTINGS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SURFACE_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    SAMPLING_FACTOR_FIELD_NUMBER: _ClassVar[int]
    STRIPE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_MEMBER_ECCENTRICITY_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_SECTION_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    NEGLECT_EQUILIBRIUM_OF_MOMENTS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_PARALLEL_TO_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_LINES_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_PARALLEL_TO_LINES_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_NODES_FIELD_NUMBER: _ClassVar[int]
    LOADED_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    LOADED_LINES_FIELD_NUMBER: _ClassVar[int]
    LOADED_NODES_FIELD_NUMBER: _ClassVar[int]
    NURBS_CONTROL_POINT_COUNT_IN_DIRECTION_U_FIELD_NUMBER: _ClassVar[int]
    NURBS_CONTROL_POINT_COUNT_IN_DIRECTION_V_FIELD_NUMBER: _ClassVar[int]
    NURBS_ORDER_IN_DIRECTION_U_FIELD_NUMBER: _ClassVar[int]
    NURBS_ORDER_IN_DIRECTION_V_FIELD_NUMBER: _ClassVar[int]
    NURBS_CONTROL_POINTS_FIELD_NUMBER: _ClassVar[int]
    QUADRANGLE_CORNER_NODES_FIELD_NUMBER: _ClassVar[int]
    QUADRANGLE_CORNER_NODE_1_FIELD_NUMBER: _ClassVar[int]
    QUADRANGLE_CORNER_NODE_2_FIELD_NUMBER: _ClassVar[int]
    QUADRANGLE_CORNER_NODE_3_FIELD_NUMBER: _ClassVar[int]
    QUADRANGLE_CORNER_NODE_4_FIELD_NUMBER: _ClassVar[int]
    QUADRANGLE_PREFERABLE_SHAPE_FIELD_NUMBER: _ClassVar[int]
    PIPE_RADIUS_FIELD_NUMBER: _ClassVar[int]
    PIPE_USE_RADIUS_END_FIELD_NUMBER: _ClassVar[int]
    PIPE_RADIUS_END_FIELD_NUMBER: _ClassVar[int]
    PIPE_CENTER_LINE_FIELD_NUMBER: _ClassVar[int]
    PIPE_GENERATED_LINES_FIELD_NUMBER: _ClassVar[int]
    HAS_LINE_HINGES_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_FIELD_NUMBER: _ClassVar[int]
    MESH_REFINEMENT_FIELD_NUMBER: _ClassVar[int]
    MESHING_TYPE_FIELD_NUMBER: _ClassVar[int]
    INPUT_AXES_ROTATION_SPECIFICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    INPUT_AXES_ANGULAR_ROTATION_FIELD_NUMBER: _ClassVar[int]
    INPUT_AXES_AXIS_FIELD_NUMBER: _ClassVar[int]
    INPUT_AXES_LINES_FIELD_NUMBER: _ClassVar[int]
    INPUT_AXES_POINT_1_FIELD_NUMBER: _ClassVar[int]
    INPUT_AXES_POINT_1_X_FIELD_NUMBER: _ClassVar[int]
    INPUT_AXES_POINT_1_Y_FIELD_NUMBER: _ClassVar[int]
    INPUT_AXES_POINT_1_Z_FIELD_NUMBER: _ClassVar[int]
    INPUT_AXES_POINT_2_FIELD_NUMBER: _ClassVar[int]
    INPUT_AXES_POINT_2_X_FIELD_NUMBER: _ClassVar[int]
    INPUT_AXES_POINT_2_Y_FIELD_NUMBER: _ClassVar[int]
    INPUT_AXES_POINT_2_Z_FIELD_NUMBER: _ClassVar[int]
    INPUT_AXES_COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    RESULT_AXES_ROTATION_SPECIFICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    REVERSED_NORMAL_FIELD_NUMBER: _ClassVar[int]
    GRID_TYPE_FIELD_NUMBER: _ClassVar[int]
    GRID_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    GRID_ORIGIN_X_FIELD_NUMBER: _ClassVar[int]
    GRID_ORIGIN_Y_FIELD_NUMBER: _ClassVar[int]
    GRID_ORIGIN_Z_FIELD_NUMBER: _ClassVar[int]
    GRID_ADAPT_AUTOMATICALLY_FIELD_NUMBER: _ClassVar[int]
    GRID_POINT_COUNT_NEGATIVE_X_FIELD_NUMBER: _ClassVar[int]
    GRID_POINT_COUNT_POSITIVE_X_FIELD_NUMBER: _ClassVar[int]
    GRID_POINT_COUNT_NEGATIVE_Y_FIELD_NUMBER: _ClassVar[int]
    GRID_POINT_COUNT_POSITIVE_Y_FIELD_NUMBER: _ClassVar[int]
    GRID_NUMBERING_INCREMENT_FIELD_NUMBER: _ClassVar[int]
    GRID_POINT_COUNT_R_FIELD_NUMBER: _ClassVar[int]
    GRID_DISTANCE_X_FIELD_NUMBER: _ClassVar[int]
    GRID_DISTANCE_Y_FIELD_NUMBER: _ClassVar[int]
    GRID_DISTANCE_R_FIELD_NUMBER: _ClassVar[int]
    GRID_ROTATION_ALPHA_FIELD_NUMBER: _ClassVar[int]
    GRID_ROTATION_BETA_FIELD_NUMBER: _ClassVar[int]
    GRID_ANGLE_GAMMA_FIELD_NUMBER: _ClassVar[int]
    AUTO_DETECTION_OF_INTEGRATED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    INTEGRATED_NODES_FIELD_NUMBER: _ClassVar[int]
    INTEGRATED_LINES_FIELD_NUMBER: _ClassVar[int]
    INTEGRATED_OPENINGS_FIELD_NUMBER: _ClassVar[int]
    HAS_INTEGRATED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    HAS_INPUT_AXES_ROTATION_FIELD_NUMBER: _ClassVar[int]
    HAS_RESULT_AXES_ROTATION_FIELD_NUMBER: _ClassVar[int]
    SURFACE_TIMBER_DESIGN_ULS_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SURFACE_TIMBER_DESIGN_SLS_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SURFACE_TIMBER_DESIGN_FR_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    TIMBER_SERVICE_CLASS_FIELD_NUMBER: _ClassVar[int]
    TIMBER_MOISTURE_CLASS_FIELD_NUMBER: _ClassVar[int]
    TIMBER_SERVICE_CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    SURFACE_REINFORCEMENTS_FIELD_NUMBER: _ClassVar[int]
    IS_USER_DEFINED_CONCRETE_COVER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_TOP_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_CONCRETE_COVER_TOP_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_CONCRETE_COVER_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_DURABILITY_TOP_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_DURABILITY_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    REINFORCEMENT_DIRECTION_TOP_FIELD_NUMBER: _ClassVar[int]
    REINFORCEMENT_DIRECTION_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_SURFACE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_DISPLACEMENT_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_LENGTH_Z_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_LENGTH_Z_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_PLANE_POINT_1_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_PLANE_POINT_1_X_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_PLANE_POINT_1_Y_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_PLANE_POINT_1_Z_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_PLANE_POINT_2_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_PLANE_POINT_2_X_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_PLANE_POINT_2_Y_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_PLANE_POINT_2_Z_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_PLANE_POINT_3_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_PLANE_POINT_3_X_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_PLANE_POINT_3_Y_FIELD_NUMBER: _ClassVar[int]
    DEFLECTION_CHECK_REFERENCE_PLANE_POINT_3_Z_FIELD_NUMBER: _ClassVar[int]
    SURFACE_REINFORCEMENT_TABLE_FIELD_NUMBER: _ClassVar[int]
    SURFACE_CONCRETE_DESIGN_ULS_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SURFACE_CONCRETE_DESIGN_SLS_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SURFACE_CONCRETE_DESIGN_FR_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SURFACE_CONCRETE_DESIGN_SEISMIC_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    ROTATED_BOUNDARY_LINE_FIELD_NUMBER: _ClassVar[int]
    ROTATED_ANGLE_OF_ROTATION_FIELD_NUMBER: _ClassVar[int]
    ROTATED_POINT_P_FIELD_NUMBER: _ClassVar[int]
    ROTATED_POINT_P_X_FIELD_NUMBER: _ClassVar[int]
    ROTATED_POINT_P_Y_FIELD_NUMBER: _ClassVar[int]
    ROTATED_POINT_P_Z_FIELD_NUMBER: _ClassVar[int]
    ROTATED_POINT_R_FIELD_NUMBER: _ClassVar[int]
    ROTATED_POINT_R_X_FIELD_NUMBER: _ClassVar[int]
    ROTATED_POINT_R_Y_FIELD_NUMBER: _ClassVar[int]
    ROTATED_POINT_R_Z_FIELD_NUMBER: _ClassVar[int]
    ROTATED_GENERATED_LINES_FIELD_NUMBER: _ClassVar[int]
    STRESS_ANALYSIS_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    geometry: SurfaceGeometry
    type: SurfaceType
    boundary_lines: _containers.RepeatedScalarFieldContainer[int]
    thickness: int
    material: int
    analytical_area: float
    analytical_volume: float
    analytical_mass: float
    analytical_center_of_gravity: _common_pb2.Vector3d
    analytical_center_of_gravity_x: float
    analytical_center_of_gravity_y: float
    analytical_center_of_gravity_z: float
    area: float
    volume: float
    mass: float
    center_of_gravity: _common_pb2.Vector3d
    center_of_gravity_x: float
    center_of_gravity_y: float
    center_of_gravity_z: float
    position: str
    position_short: str
    grid_enabled: bool
    is_deactivated_for_calculation: bool
    comment: str
    design_properties_via_surface: bool
    design_properties_via_parent_surface_set: bool
    design_properties_parent_surface_set: int
    load_transfer_direction: SurfaceLoadTransferDirection
    is_surface_weight_enabled: bool
    is_advanced_distribution_settings_enabled: bool
    surface_weight: float
    sampling_factor: float
    stripe_width: float
    consider_member_eccentricity: bool
    consider_section_distribution: bool
    load_distribution: SurfaceLoadDistribution
    neglect_equilibrium_of_moments: bool
    excluded_members: _containers.RepeatedScalarFieldContainer[int]
    excluded_parallel_to_members: _containers.RepeatedScalarFieldContainer[int]
    excluded_lines: _containers.RepeatedScalarFieldContainer[int]
    excluded_parallel_to_lines: _containers.RepeatedScalarFieldContainer[int]
    excluded_nodes: _containers.RepeatedScalarFieldContainer[int]
    loaded_members: _containers.RepeatedScalarFieldContainer[int]
    loaded_lines: _containers.RepeatedScalarFieldContainer[int]
    loaded_nodes: _containers.RepeatedScalarFieldContainer[int]
    nurbs_control_point_count_in_direction_u: int
    nurbs_control_point_count_in_direction_v: int
    nurbs_order_in_direction_u: int
    nurbs_order_in_direction_v: int
    nurbs_control_points: SurfaceNurbsControlPointsRowsTable
    quadrangle_corner_nodes: _containers.RepeatedScalarFieldContainer[int]
    quadrangle_corner_node_1: int
    quadrangle_corner_node_2: int
    quadrangle_corner_node_3: int
    quadrangle_corner_node_4: int
    quadrangle_preferable_shape: SurfaceQuadranglePreferableShape
    pipe_radius: float
    pipe_use_radius_end: bool
    pipe_radius_end: float
    pipe_center_line: int
    pipe_generated_lines: _containers.RepeatedScalarFieldContainer[int]
    has_line_hinges: bool
    support: int
    eccentricity: int
    mesh_refinement: int
    meshing_type: SurfaceMeshingType
    input_axes_rotation_specification_type: SurfaceInputAxesRotationSpecificationType
    input_axes_angular_rotation: float
    input_axes_axis: SurfaceInputAxesAxis
    input_axes_lines: _containers.RepeatedScalarFieldContainer[int]
    input_axes_point_1: _common_pb2.Vector3d
    input_axes_point_1_x: float
    input_axes_point_1_y: float
    input_axes_point_1_z: float
    input_axes_point_2: _common_pb2.Vector3d
    input_axes_point_2_x: float
    input_axes_point_2_y: float
    input_axes_point_2_z: float
    input_axes_coordinate_system: int
    result_axes_rotation_specification_type: SurfaceResultAxesRotationSpecificationType
    reversed_normal: bool
    grid_type: SurfaceGridType
    grid_origin: _common_pb2.Vector3d
    grid_origin_x: float
    grid_origin_y: float
    grid_origin_z: float
    grid_adapt_automatically: bool
    grid_point_count_negative_x: int
    grid_point_count_positive_x: int
    grid_point_count_negative_y: int
    grid_point_count_positive_y: int
    grid_numbering_increment: int
    grid_point_count_r: int
    grid_distance_x: float
    grid_distance_y: float
    grid_distance_r: float
    grid_rotation_alpha: float
    grid_rotation_beta: float
    grid_angle_gamma: float
    auto_detection_of_integrated_objects: bool
    integrated_nodes: _containers.RepeatedScalarFieldContainer[int]
    integrated_lines: _containers.RepeatedScalarFieldContainer[int]
    integrated_openings: _containers.RepeatedScalarFieldContainer[int]
    has_integrated_objects: bool
    has_input_axes_rotation: bool
    has_result_axes_rotation: bool
    surface_timber_design_uls_configuration: int
    surface_timber_design_sls_configuration: int
    surface_timber_design_fr_configuration: int
    timber_service_class: int
    timber_moisture_class: int
    timber_service_conditions: int
    surface_reinforcements: _containers.RepeatedScalarFieldContainer[int]
    is_user_defined_concrete_cover_enabled: bool
    concrete_cover_top: float
    concrete_cover_bottom: float
    user_defined_concrete_cover_top: float
    user_defined_concrete_cover_bottom: float
    concrete_durability_top: int
    concrete_durability_bottom: int
    reinforcement_direction_top: int
    reinforcement_direction_bottom: int
    deflection_check_surface_type: SurfaceDeflectionCheckSurfaceType
    deflection_check_displacement_reference: SurfaceDeflectionCheckDisplacementReference
    deflection_check_reference_length_z: float
    deflection_check_reference_length_z_definition_type: SurfaceDeflectionCheckReferenceLengthZDefinitionType
    deflection_check_reference_plane_point_1: _common_pb2.Vector3d
    deflection_check_reference_plane_point_1_x: float
    deflection_check_reference_plane_point_1_y: float
    deflection_check_reference_plane_point_1_z: float
    deflection_check_reference_plane_point_2: _common_pb2.Vector3d
    deflection_check_reference_plane_point_2_x: float
    deflection_check_reference_plane_point_2_y: float
    deflection_check_reference_plane_point_2_z: float
    deflection_check_reference_plane_point_3: _common_pb2.Vector3d
    deflection_check_reference_plane_point_3_x: float
    deflection_check_reference_plane_point_3_y: float
    deflection_check_reference_plane_point_3_z: float
    surface_reinforcement_table: SurfaceSurfaceReinforcementTable
    surface_concrete_design_uls_configuration: int
    surface_concrete_design_sls_configuration: int
    surface_concrete_design_fr_configuration: int
    surface_concrete_design_seismic_configuration: int
    rotated_boundary_line: int
    rotated_angle_of_rotation: float
    rotated_point_p: _common_pb2.Vector3d
    rotated_point_p_x: float
    rotated_point_p_y: float
    rotated_point_p_z: float
    rotated_point_r: _common_pb2.Vector3d
    rotated_point_r_x: float
    rotated_point_r_y: float
    rotated_point_r_z: float
    rotated_generated_lines: _containers.RepeatedScalarFieldContainer[int]
    stress_analysis_configuration: int
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., geometry: _Optional[_Union[SurfaceGeometry, str]] = ..., type: _Optional[_Union[SurfaceType, str]] = ..., boundary_lines: _Optional[_Iterable[int]] = ..., thickness: _Optional[int] = ..., material: _Optional[int] = ..., analytical_area: _Optional[float] = ..., analytical_volume: _Optional[float] = ..., analytical_mass: _Optional[float] = ..., analytical_center_of_gravity: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., analytical_center_of_gravity_x: _Optional[float] = ..., analytical_center_of_gravity_y: _Optional[float] = ..., analytical_center_of_gravity_z: _Optional[float] = ..., area: _Optional[float] = ..., volume: _Optional[float] = ..., mass: _Optional[float] = ..., center_of_gravity: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., center_of_gravity_x: _Optional[float] = ..., center_of_gravity_y: _Optional[float] = ..., center_of_gravity_z: _Optional[float] = ..., position: _Optional[str] = ..., position_short: _Optional[str] = ..., grid_enabled: bool = ..., is_deactivated_for_calculation: bool = ..., comment: _Optional[str] = ..., design_properties_via_surface: bool = ..., design_properties_via_parent_surface_set: bool = ..., design_properties_parent_surface_set: _Optional[int] = ..., load_transfer_direction: _Optional[_Union[SurfaceLoadTransferDirection, str]] = ..., is_surface_weight_enabled: bool = ..., is_advanced_distribution_settings_enabled: bool = ..., surface_weight: _Optional[float] = ..., sampling_factor: _Optional[float] = ..., stripe_width: _Optional[float] = ..., consider_member_eccentricity: bool = ..., consider_section_distribution: bool = ..., load_distribution: _Optional[_Union[SurfaceLoadDistribution, str]] = ..., neglect_equilibrium_of_moments: bool = ..., excluded_members: _Optional[_Iterable[int]] = ..., excluded_parallel_to_members: _Optional[_Iterable[int]] = ..., excluded_lines: _Optional[_Iterable[int]] = ..., excluded_parallel_to_lines: _Optional[_Iterable[int]] = ..., excluded_nodes: _Optional[_Iterable[int]] = ..., loaded_members: _Optional[_Iterable[int]] = ..., loaded_lines: _Optional[_Iterable[int]] = ..., loaded_nodes: _Optional[_Iterable[int]] = ..., nurbs_control_point_count_in_direction_u: _Optional[int] = ..., nurbs_control_point_count_in_direction_v: _Optional[int] = ..., nurbs_order_in_direction_u: _Optional[int] = ..., nurbs_order_in_direction_v: _Optional[int] = ..., nurbs_control_points: _Optional[_Union[SurfaceNurbsControlPointsRowsTable, _Mapping]] = ..., quadrangle_corner_nodes: _Optional[_Iterable[int]] = ..., quadrangle_corner_node_1: _Optional[int] = ..., quadrangle_corner_node_2: _Optional[int] = ..., quadrangle_corner_node_3: _Optional[int] = ..., quadrangle_corner_node_4: _Optional[int] = ..., quadrangle_preferable_shape: _Optional[_Union[SurfaceQuadranglePreferableShape, str]] = ..., pipe_radius: _Optional[float] = ..., pipe_use_radius_end: bool = ..., pipe_radius_end: _Optional[float] = ..., pipe_center_line: _Optional[int] = ..., pipe_generated_lines: _Optional[_Iterable[int]] = ..., has_line_hinges: bool = ..., support: _Optional[int] = ..., eccentricity: _Optional[int] = ..., mesh_refinement: _Optional[int] = ..., meshing_type: _Optional[_Union[SurfaceMeshingType, str]] = ..., input_axes_rotation_specification_type: _Optional[_Union[SurfaceInputAxesRotationSpecificationType, str]] = ..., input_axes_angular_rotation: _Optional[float] = ..., input_axes_axis: _Optional[_Union[SurfaceInputAxesAxis, str]] = ..., input_axes_lines: _Optional[_Iterable[int]] = ..., input_axes_point_1: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., input_axes_point_1_x: _Optional[float] = ..., input_axes_point_1_y: _Optional[float] = ..., input_axes_point_1_z: _Optional[float] = ..., input_axes_point_2: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., input_axes_point_2_x: _Optional[float] = ..., input_axes_point_2_y: _Optional[float] = ..., input_axes_point_2_z: _Optional[float] = ..., input_axes_coordinate_system: _Optional[int] = ..., result_axes_rotation_specification_type: _Optional[_Union[SurfaceResultAxesRotationSpecificationType, str]] = ..., reversed_normal: bool = ..., grid_type: _Optional[_Union[SurfaceGridType, str]] = ..., grid_origin: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., grid_origin_x: _Optional[float] = ..., grid_origin_y: _Optional[float] = ..., grid_origin_z: _Optional[float] = ..., grid_adapt_automatically: bool = ..., grid_point_count_negative_x: _Optional[int] = ..., grid_point_count_positive_x: _Optional[int] = ..., grid_point_count_negative_y: _Optional[int] = ..., grid_point_count_positive_y: _Optional[int] = ..., grid_numbering_increment: _Optional[int] = ..., grid_point_count_r: _Optional[int] = ..., grid_distance_x: _Optional[float] = ..., grid_distance_y: _Optional[float] = ..., grid_distance_r: _Optional[float] = ..., grid_rotation_alpha: _Optional[float] = ..., grid_rotation_beta: _Optional[float] = ..., grid_angle_gamma: _Optional[float] = ..., auto_detection_of_integrated_objects: bool = ..., integrated_nodes: _Optional[_Iterable[int]] = ..., integrated_lines: _Optional[_Iterable[int]] = ..., integrated_openings: _Optional[_Iterable[int]] = ..., has_integrated_objects: bool = ..., has_input_axes_rotation: bool = ..., has_result_axes_rotation: bool = ..., surface_timber_design_uls_configuration: _Optional[int] = ..., surface_timber_design_sls_configuration: _Optional[int] = ..., surface_timber_design_fr_configuration: _Optional[int] = ..., timber_service_class: _Optional[int] = ..., timber_moisture_class: _Optional[int] = ..., timber_service_conditions: _Optional[int] = ..., surface_reinforcements: _Optional[_Iterable[int]] = ..., is_user_defined_concrete_cover_enabled: bool = ..., concrete_cover_top: _Optional[float] = ..., concrete_cover_bottom: _Optional[float] = ..., user_defined_concrete_cover_top: _Optional[float] = ..., user_defined_concrete_cover_bottom: _Optional[float] = ..., concrete_durability_top: _Optional[int] = ..., concrete_durability_bottom: _Optional[int] = ..., reinforcement_direction_top: _Optional[int] = ..., reinforcement_direction_bottom: _Optional[int] = ..., deflection_check_surface_type: _Optional[_Union[SurfaceDeflectionCheckSurfaceType, str]] = ..., deflection_check_displacement_reference: _Optional[_Union[SurfaceDeflectionCheckDisplacementReference, str]] = ..., deflection_check_reference_length_z: _Optional[float] = ..., deflection_check_reference_length_z_definition_type: _Optional[_Union[SurfaceDeflectionCheckReferenceLengthZDefinitionType, str]] = ..., deflection_check_reference_plane_point_1: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., deflection_check_reference_plane_point_1_x: _Optional[float] = ..., deflection_check_reference_plane_point_1_y: _Optional[float] = ..., deflection_check_reference_plane_point_1_z: _Optional[float] = ..., deflection_check_reference_plane_point_2: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., deflection_check_reference_plane_point_2_x: _Optional[float] = ..., deflection_check_reference_plane_point_2_y: _Optional[float] = ..., deflection_check_reference_plane_point_2_z: _Optional[float] = ..., deflection_check_reference_plane_point_3: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., deflection_check_reference_plane_point_3_x: _Optional[float] = ..., deflection_check_reference_plane_point_3_y: _Optional[float] = ..., deflection_check_reference_plane_point_3_z: _Optional[float] = ..., surface_reinforcement_table: _Optional[_Union[SurfaceSurfaceReinforcementTable, _Mapping]] = ..., surface_concrete_design_uls_configuration: _Optional[int] = ..., surface_concrete_design_sls_configuration: _Optional[int] = ..., surface_concrete_design_fr_configuration: _Optional[int] = ..., surface_concrete_design_seismic_configuration: _Optional[int] = ..., rotated_boundary_line: _Optional[int] = ..., rotated_angle_of_rotation: _Optional[float] = ..., rotated_point_p: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., rotated_point_p_x: _Optional[float] = ..., rotated_point_p_y: _Optional[float] = ..., rotated_point_p_z: _Optional[float] = ..., rotated_point_r: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., rotated_point_r_x: _Optional[float] = ..., rotated_point_r_y: _Optional[float] = ..., rotated_point_r_z: _Optional[float] = ..., rotated_generated_lines: _Optional[_Iterable[int]] = ..., stress_analysis_configuration: _Optional[int] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class SurfaceNurbsControlPointsRowsTable(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SurfaceSurfaceReinforcementTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[SurfaceSurfaceReinforcementTableRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[SurfaceSurfaceReinforcementTableRow, _Mapping]]] = ...) -> None: ...

class SurfaceSurfaceReinforcementTableRow(_message.Message):
    __slots__ = ("no", "description", "surface_reinforcement")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SURFACE_REINFORCEMENT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    surface_reinforcement: int
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., surface_reinforcement: _Optional[int] = ...) -> None: ...
