from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberLoadLoadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_LOAD_TYPE_UNKNOWN: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_E_TYPE_MASS: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_AXIAL_DISPLACEMENT: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_AXIAL_STRAIN: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_COATING_CONTOUR: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_COATING_POLYGON: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_DISPLACEMENT: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_END_PRESTRESS: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_FORCE: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_FORM_FINDING: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_INITIAL_PRESTRESS: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_MOMENT: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_PIPE_CONTENT_FULL: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_PIPE_CONTENT_PARTIAL: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_PIPE_INTERNAL_PRESSURE: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_PRECAMBER: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_ROTARY_MOTION: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_ROTATION: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_TEMPERATURE: _ClassVar[MemberLoadLoadType]
    MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_TEMPERATURE_CHANGE: _ClassVar[MemberLoadLoadType]

class MemberLoadLoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_LOAD_DISTRIBUTION_UNIFORM: _ClassVar[MemberLoadLoadDistribution]
    MEMBER_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_1: _ClassVar[MemberLoadLoadDistribution]
    MEMBER_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_2: _ClassVar[MemberLoadLoadDistribution]
    MEMBER_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_2_2: _ClassVar[MemberLoadLoadDistribution]
    MEMBER_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_N: _ClassVar[MemberLoadLoadDistribution]
    MEMBER_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_VARYING: _ClassVar[MemberLoadLoadDistribution]
    MEMBER_LOAD_LOAD_DISTRIBUTION_PARABOLIC: _ClassVar[MemberLoadLoadDistribution]
    MEMBER_LOAD_LOAD_DISTRIBUTION_TAPERED: _ClassVar[MemberLoadLoadDistribution]
    MEMBER_LOAD_LOAD_DISTRIBUTION_TRAPEZOIDAL: _ClassVar[MemberLoadLoadDistribution]
    MEMBER_LOAD_LOAD_DISTRIBUTION_UNIFORM_TOTAL: _ClassVar[MemberLoadLoadDistribution]
    MEMBER_LOAD_LOAD_DISTRIBUTION_VARYING: _ClassVar[MemberLoadLoadDistribution]
    MEMBER_LOAD_LOAD_DISTRIBUTION_VARYING_IN_Z: _ClassVar[MemberLoadLoadDistribution]

class MemberLoadLoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_LOAD_DIRECTION_LOCAL_X: _ClassVar[MemberLoadLoadDirection]
    MEMBER_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED: _ClassVar[MemberLoadLoadDirection]
    MEMBER_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE: _ClassVar[MemberLoadLoadDirection]
    MEMBER_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED: _ClassVar[MemberLoadLoadDirection]
    MEMBER_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE: _ClassVar[MemberLoadLoadDirection]
    MEMBER_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED: _ClassVar[MemberLoadLoadDirection]
    MEMBER_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE: _ClassVar[MemberLoadLoadDirection]
    MEMBER_LOAD_LOAD_DIRECTION_LOCAL_Y: _ClassVar[MemberLoadLoadDirection]
    MEMBER_LOAD_LOAD_DIRECTION_LOCAL_Z: _ClassVar[MemberLoadLoadDirection]
    MEMBER_LOAD_LOAD_DIRECTION_PRINCIPAL_U: _ClassVar[MemberLoadLoadDirection]
    MEMBER_LOAD_LOAD_DIRECTION_PRINCIPAL_V: _ClassVar[MemberLoadLoadDirection]

class MemberLoadLoadDirectionOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_FORWARD: _ClassVar[MemberLoadLoadDirectionOrientation]
    MEMBER_LOAD_LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_REVERSED: _ClassVar[MemberLoadLoadDirectionOrientation]

class MemberLoadFormFindingDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_FORM_FINDING_DEFINITION_TYPE_GEOMETRIC: _ClassVar[MemberLoadFormFindingDefinitionType]
    MEMBER_LOAD_FORM_FINDING_DEFINITION_TYPE_FORCE: _ClassVar[MemberLoadFormFindingDefinitionType]

class MemberLoadAxisDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_AXIS_DEFINITION_TYPE_TWO_POINTS: _ClassVar[MemberLoadAxisDefinitionType]
    MEMBER_LOAD_AXIS_DEFINITION_TYPE_POINT_AND_AXIS: _ClassVar[MemberLoadAxisDefinitionType]

class MemberLoadAxisDefinitionAxis(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_AXIS_DEFINITION_AXIS_X: _ClassVar[MemberLoadAxisDefinitionAxis]
    MEMBER_LOAD_AXIS_DEFINITION_AXIS_Y: _ClassVar[MemberLoadAxisDefinitionAxis]
    MEMBER_LOAD_AXIS_DEFINITION_AXIS_Z: _ClassVar[MemberLoadAxisDefinitionAxis]

class MemberLoadAxisDefinitionAxisOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_AXIS_DEFINITION_AXIS_ORIENTATION_POSITIVE: _ClassVar[MemberLoadAxisDefinitionAxisOrientation]
    MEMBER_LOAD_AXIS_DEFINITION_AXIS_ORIENTATION_NEGATIVE: _ClassVar[MemberLoadAxisDefinitionAxisOrientation]

class MemberLoadEccentricityHorizontalAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_ECCENTRICITY_HORIZONTAL_ALIGNMENT_LEFT: _ClassVar[MemberLoadEccentricityHorizontalAlignment]
    MEMBER_LOAD_ECCENTRICITY_HORIZONTAL_ALIGNMENT_CENTER: _ClassVar[MemberLoadEccentricityHorizontalAlignment]
    MEMBER_LOAD_ECCENTRICITY_HORIZONTAL_ALIGNMENT_NONE: _ClassVar[MemberLoadEccentricityHorizontalAlignment]
    MEMBER_LOAD_ECCENTRICITY_HORIZONTAL_ALIGNMENT_RIGHT: _ClassVar[MemberLoadEccentricityHorizontalAlignment]

class MemberLoadEccentricityVerticalAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_ECCENTRICITY_VERTICAL_ALIGNMENT_TOP: _ClassVar[MemberLoadEccentricityVerticalAlignment]
    MEMBER_LOAD_ECCENTRICITY_VERTICAL_ALIGNMENT_BOTTOM: _ClassVar[MemberLoadEccentricityVerticalAlignment]
    MEMBER_LOAD_ECCENTRICITY_VERTICAL_ALIGNMENT_CENTER: _ClassVar[MemberLoadEccentricityVerticalAlignment]
    MEMBER_LOAD_ECCENTRICITY_VERTICAL_ALIGNMENT_NONE: _ClassVar[MemberLoadEccentricityVerticalAlignment]

class MemberLoadEccentricitySectionMiddle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_ECCENTRICITY_SECTION_MIDDLE_CENTER_OF_GRAVITY: _ClassVar[MemberLoadEccentricitySectionMiddle]
    MEMBER_LOAD_ECCENTRICITY_SECTION_MIDDLE_NONE: _ClassVar[MemberLoadEccentricitySectionMiddle]
    MEMBER_LOAD_ECCENTRICITY_SECTION_MIDDLE_SHEAR_CENTER: _ClassVar[MemberLoadEccentricitySectionMiddle]

class MemberLoadFormFindingInternalForce(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_FORM_FINDING_INTERNAL_FORCE_TENSION: _ClassVar[MemberLoadFormFindingInternalForce]
    MEMBER_LOAD_FORM_FINDING_INTERNAL_FORCE_COMPRESSION: _ClassVar[MemberLoadFormFindingInternalForce]

class MemberLoadFormFindingGeometryDefinition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_FORM_FINDING_GEOMETRY_DEFINITION_LENGTH: _ClassVar[MemberLoadFormFindingGeometryDefinition]
    MEMBER_LOAD_FORM_FINDING_GEOMETRY_DEFINITION_LOW_POINT_VERTICAL_SAG: _ClassVar[MemberLoadFormFindingGeometryDefinition]
    MEMBER_LOAD_FORM_FINDING_GEOMETRY_DEFINITION_MAX_VERTICAL_SAG: _ClassVar[MemberLoadFormFindingGeometryDefinition]
    MEMBER_LOAD_FORM_FINDING_GEOMETRY_DEFINITION_SAG: _ClassVar[MemberLoadFormFindingGeometryDefinition]
    MEMBER_LOAD_FORM_FINDING_GEOMETRY_DEFINITION_UNSTRESSED_LENGTH: _ClassVar[MemberLoadFormFindingGeometryDefinition]

class MemberLoadFormFindingForceDefinition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_UNKNOWN: _ClassVar[MemberLoadFormFindingForceDefinition]
    MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_AVERAGE: _ClassVar[MemberLoadFormFindingForceDefinition]
    MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_DENSITY: _ClassVar[MemberLoadFormFindingForceDefinition]
    MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_HORIZONTAL_TENSION_COMPONENT: _ClassVar[MemberLoadFormFindingForceDefinition]
    MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_MAX_FORCE_MEMBER: _ClassVar[MemberLoadFormFindingForceDefinition]
    MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_MINIMAL_TENSION_AT_IEND: _ClassVar[MemberLoadFormFindingForceDefinition]
    MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_MINIMAL_TENSION_AT_JEND: _ClassVar[MemberLoadFormFindingForceDefinition]
    MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_MIN_FORCE_MEMBER: _ClassVar[MemberLoadFormFindingForceDefinition]
    MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_TENSION_AT_IEND: _ClassVar[MemberLoadFormFindingForceDefinition]
    MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_TENSION_AT_JEND: _ClassVar[MemberLoadFormFindingForceDefinition]
MEMBER_LOAD_LOAD_TYPE_UNKNOWN: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_E_TYPE_MASS: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_AXIAL_DISPLACEMENT: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_AXIAL_STRAIN: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_COATING_CONTOUR: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_COATING_POLYGON: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_DISPLACEMENT: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_END_PRESTRESS: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_FORCE: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_FORM_FINDING: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_INITIAL_PRESTRESS: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_MOMENT: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_PIPE_CONTENT_FULL: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_PIPE_CONTENT_PARTIAL: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_PIPE_INTERNAL_PRESSURE: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_PRECAMBER: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_ROTARY_MOTION: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_ROTATION: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_TEMPERATURE: MemberLoadLoadType
MEMBER_LOAD_LOAD_TYPE_LOAD_TYPE_TEMPERATURE_CHANGE: MemberLoadLoadType
MEMBER_LOAD_LOAD_DISTRIBUTION_UNIFORM: MemberLoadLoadDistribution
MEMBER_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_1: MemberLoadLoadDistribution
MEMBER_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_2: MemberLoadLoadDistribution
MEMBER_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_2_2: MemberLoadLoadDistribution
MEMBER_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_N: MemberLoadLoadDistribution
MEMBER_LOAD_LOAD_DISTRIBUTION_CONCENTRATED_VARYING: MemberLoadLoadDistribution
MEMBER_LOAD_LOAD_DISTRIBUTION_PARABOLIC: MemberLoadLoadDistribution
MEMBER_LOAD_LOAD_DISTRIBUTION_TAPERED: MemberLoadLoadDistribution
MEMBER_LOAD_LOAD_DISTRIBUTION_TRAPEZOIDAL: MemberLoadLoadDistribution
MEMBER_LOAD_LOAD_DISTRIBUTION_UNIFORM_TOTAL: MemberLoadLoadDistribution
MEMBER_LOAD_LOAD_DISTRIBUTION_VARYING: MemberLoadLoadDistribution
MEMBER_LOAD_LOAD_DISTRIBUTION_VARYING_IN_Z: MemberLoadLoadDistribution
MEMBER_LOAD_LOAD_DIRECTION_LOCAL_X: MemberLoadLoadDirection
MEMBER_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED: MemberLoadLoadDirection
MEMBER_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE: MemberLoadLoadDirection
MEMBER_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED: MemberLoadLoadDirection
MEMBER_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE: MemberLoadLoadDirection
MEMBER_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED: MemberLoadLoadDirection
MEMBER_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE: MemberLoadLoadDirection
MEMBER_LOAD_LOAD_DIRECTION_LOCAL_Y: MemberLoadLoadDirection
MEMBER_LOAD_LOAD_DIRECTION_LOCAL_Z: MemberLoadLoadDirection
MEMBER_LOAD_LOAD_DIRECTION_PRINCIPAL_U: MemberLoadLoadDirection
MEMBER_LOAD_LOAD_DIRECTION_PRINCIPAL_V: MemberLoadLoadDirection
MEMBER_LOAD_LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_FORWARD: MemberLoadLoadDirectionOrientation
MEMBER_LOAD_LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_REVERSED: MemberLoadLoadDirectionOrientation
MEMBER_LOAD_FORM_FINDING_DEFINITION_TYPE_GEOMETRIC: MemberLoadFormFindingDefinitionType
MEMBER_LOAD_FORM_FINDING_DEFINITION_TYPE_FORCE: MemberLoadFormFindingDefinitionType
MEMBER_LOAD_AXIS_DEFINITION_TYPE_TWO_POINTS: MemberLoadAxisDefinitionType
MEMBER_LOAD_AXIS_DEFINITION_TYPE_POINT_AND_AXIS: MemberLoadAxisDefinitionType
MEMBER_LOAD_AXIS_DEFINITION_AXIS_X: MemberLoadAxisDefinitionAxis
MEMBER_LOAD_AXIS_DEFINITION_AXIS_Y: MemberLoadAxisDefinitionAxis
MEMBER_LOAD_AXIS_DEFINITION_AXIS_Z: MemberLoadAxisDefinitionAxis
MEMBER_LOAD_AXIS_DEFINITION_AXIS_ORIENTATION_POSITIVE: MemberLoadAxisDefinitionAxisOrientation
MEMBER_LOAD_AXIS_DEFINITION_AXIS_ORIENTATION_NEGATIVE: MemberLoadAxisDefinitionAxisOrientation
MEMBER_LOAD_ECCENTRICITY_HORIZONTAL_ALIGNMENT_LEFT: MemberLoadEccentricityHorizontalAlignment
MEMBER_LOAD_ECCENTRICITY_HORIZONTAL_ALIGNMENT_CENTER: MemberLoadEccentricityHorizontalAlignment
MEMBER_LOAD_ECCENTRICITY_HORIZONTAL_ALIGNMENT_NONE: MemberLoadEccentricityHorizontalAlignment
MEMBER_LOAD_ECCENTRICITY_HORIZONTAL_ALIGNMENT_RIGHT: MemberLoadEccentricityHorizontalAlignment
MEMBER_LOAD_ECCENTRICITY_VERTICAL_ALIGNMENT_TOP: MemberLoadEccentricityVerticalAlignment
MEMBER_LOAD_ECCENTRICITY_VERTICAL_ALIGNMENT_BOTTOM: MemberLoadEccentricityVerticalAlignment
MEMBER_LOAD_ECCENTRICITY_VERTICAL_ALIGNMENT_CENTER: MemberLoadEccentricityVerticalAlignment
MEMBER_LOAD_ECCENTRICITY_VERTICAL_ALIGNMENT_NONE: MemberLoadEccentricityVerticalAlignment
MEMBER_LOAD_ECCENTRICITY_SECTION_MIDDLE_CENTER_OF_GRAVITY: MemberLoadEccentricitySectionMiddle
MEMBER_LOAD_ECCENTRICITY_SECTION_MIDDLE_NONE: MemberLoadEccentricitySectionMiddle
MEMBER_LOAD_ECCENTRICITY_SECTION_MIDDLE_SHEAR_CENTER: MemberLoadEccentricitySectionMiddle
MEMBER_LOAD_FORM_FINDING_INTERNAL_FORCE_TENSION: MemberLoadFormFindingInternalForce
MEMBER_LOAD_FORM_FINDING_INTERNAL_FORCE_COMPRESSION: MemberLoadFormFindingInternalForce
MEMBER_LOAD_FORM_FINDING_GEOMETRY_DEFINITION_LENGTH: MemberLoadFormFindingGeometryDefinition
MEMBER_LOAD_FORM_FINDING_GEOMETRY_DEFINITION_LOW_POINT_VERTICAL_SAG: MemberLoadFormFindingGeometryDefinition
MEMBER_LOAD_FORM_FINDING_GEOMETRY_DEFINITION_MAX_VERTICAL_SAG: MemberLoadFormFindingGeometryDefinition
MEMBER_LOAD_FORM_FINDING_GEOMETRY_DEFINITION_SAG: MemberLoadFormFindingGeometryDefinition
MEMBER_LOAD_FORM_FINDING_GEOMETRY_DEFINITION_UNSTRESSED_LENGTH: MemberLoadFormFindingGeometryDefinition
MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_UNKNOWN: MemberLoadFormFindingForceDefinition
MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_AVERAGE: MemberLoadFormFindingForceDefinition
MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_DENSITY: MemberLoadFormFindingForceDefinition
MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_HORIZONTAL_TENSION_COMPONENT: MemberLoadFormFindingForceDefinition
MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_MAX_FORCE_MEMBER: MemberLoadFormFindingForceDefinition
MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_MINIMAL_TENSION_AT_IEND: MemberLoadFormFindingForceDefinition
MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_MINIMAL_TENSION_AT_JEND: MemberLoadFormFindingForceDefinition
MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_MIN_FORCE_MEMBER: MemberLoadFormFindingForceDefinition
MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_TENSION_AT_IEND: MemberLoadFormFindingForceDefinition
MEMBER_LOAD_FORM_FINDING_FORCE_DEFINITION_TENSION_AT_JEND: MemberLoadFormFindingForceDefinition

class MemberLoad(_message.Message):
    __slots__ = ("no", "load_type", "reference_to_list_of_members", "members", "load_case", "coordinate_system", "load_distribution", "load_direction", "load_direction_orientation", "form_finding_definition_type", "magnitude", "magnitude_1", "magnitude_2", "magnitude_3", "magnitude_t_c", "magnitude_t_c_1", "magnitude_t_c_2", "magnitude_t_c_3", "magnitude_delta_t", "magnitude_delta_t_1", "magnitude_delta_t_2", "magnitude_delta_t_3", "magnitude_t_t", "magnitude_t_t_1", "magnitude_t_t_2", "magnitude_t_t_3", "magnitude_t_b", "magnitude_t_b_1", "magnitude_t_b_2", "magnitude_t_b_3", "individual_mass_components", "mass_global", "mass_x", "mass_y", "mass_z", "distance_a_is_defined_as_relative", "distance_a_absolute", "distance_a_relative", "distance_b_is_defined_as_relative", "distance_b_absolute", "distance_b_relative", "distance_c_is_defined_as_relative", "distance_c_absolute", "distance_c_relative", "count_n", "varying_load_parameters_are_defined_as_relative", "varying_load_parameters", "varying_load_parameters_sorted", "angular_velocity", "angular_acceleration", "axis_definition_type", "axis_definition_p1", "axis_definition_p1_x", "axis_definition_p1_y", "axis_definition_p1_z", "axis_definition_p2", "axis_definition_p2_x", "axis_definition_p2_y", "axis_definition_p2_z", "axis_definition_axis", "axis_definition_axis_orientation", "filling_height", "distance_from_member_end", "load_is_over_total_length", "has_force_eccentricity", "eccentricity_horizontal_alignment", "eccentricity_vertical_alignment", "eccentricity_section_middle", "is_eccentricity_at_end_different_from_start", "eccentricity_y_at_start", "eccentricity_z_at_start", "eccentricity_y_at_end", "eccentricity_z_at_end", "comment", "is_generated", "generating_object_info", "form_finding_internal_force", "form_finding_geometry_definition", "form_finding_force_definition", "form_finding_magnitude_is_defined_as_relative", "form_finding_magnitude_absolute", "form_finding_magnitude_relative", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    LOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_TO_LIST_OF_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    LOAD_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_3_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_C_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_C_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_C_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_C_3_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_DELTA_T_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_DELTA_T_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_DELTA_T_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_DELTA_T_3_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_T_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_T_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_T_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_T_3_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_B_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_B_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_B_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_B_3_FIELD_NUMBER: _ClassVar[int]
    INDIVIDUAL_MASS_COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    MASS_GLOBAL_FIELD_NUMBER: _ClassVar[int]
    MASS_X_FIELD_NUMBER: _ClassVar[int]
    MASS_Y_FIELD_NUMBER: _ClassVar[int]
    MASS_Z_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_A_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_A_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_A_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_B_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_B_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_B_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_C_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_C_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_C_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    COUNT_N_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_ARE_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_SORTED_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_X_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_Y_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_Z_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_X_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_Y_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_Z_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_AXIS_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_AXIS_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    FILLING_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FROM_MEMBER_END_FIELD_NUMBER: _ClassVar[int]
    LOAD_IS_OVER_TOTAL_LENGTH_FIELD_NUMBER: _ClassVar[int]
    HAS_FORCE_ECCENTRICITY_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_HORIZONTAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_VERTICAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_SECTION_MIDDLE_FIELD_NUMBER: _ClassVar[int]
    IS_ECCENTRICITY_AT_END_DIFFERENT_FROM_START_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_Y_AT_START_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_Z_AT_START_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_Y_AT_END_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_Z_AT_END_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_INTERNAL_FORCE_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_GEOMETRY_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_FORCE_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_MAGNITUDE_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_MAGNITUDE_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_MAGNITUDE_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    load_type: MemberLoadLoadType
    reference_to_list_of_members: bool
    members: _containers.RepeatedScalarFieldContainer[int]
    load_case: int
    coordinate_system: str
    load_distribution: MemberLoadLoadDistribution
    load_direction: MemberLoadLoadDirection
    load_direction_orientation: MemberLoadLoadDirectionOrientation
    form_finding_definition_type: MemberLoadFormFindingDefinitionType
    magnitude: float
    magnitude_1: float
    magnitude_2: float
    magnitude_3: float
    magnitude_t_c: float
    magnitude_t_c_1: float
    magnitude_t_c_2: float
    magnitude_t_c_3: float
    magnitude_delta_t: float
    magnitude_delta_t_1: float
    magnitude_delta_t_2: float
    magnitude_delta_t_3: float
    magnitude_t_t: float
    magnitude_t_t_1: float
    magnitude_t_t_2: float
    magnitude_t_t_3: float
    magnitude_t_b: float
    magnitude_t_b_1: float
    magnitude_t_b_2: float
    magnitude_t_b_3: float
    individual_mass_components: bool
    mass_global: float
    mass_x: float
    mass_y: float
    mass_z: float
    distance_a_is_defined_as_relative: bool
    distance_a_absolute: float
    distance_a_relative: float
    distance_b_is_defined_as_relative: bool
    distance_b_absolute: float
    distance_b_relative: float
    distance_c_is_defined_as_relative: bool
    distance_c_absolute: float
    distance_c_relative: float
    count_n: int
    varying_load_parameters_are_defined_as_relative: bool
    varying_load_parameters: MemberLoadVaryingLoadParametersTable
    varying_load_parameters_sorted: bool
    angular_velocity: float
    angular_acceleration: float
    axis_definition_type: MemberLoadAxisDefinitionType
    axis_definition_p1: _common_pb2.Vector3d
    axis_definition_p1_x: float
    axis_definition_p1_y: float
    axis_definition_p1_z: float
    axis_definition_p2: _common_pb2.Vector3d
    axis_definition_p2_x: float
    axis_definition_p2_y: float
    axis_definition_p2_z: float
    axis_definition_axis: MemberLoadAxisDefinitionAxis
    axis_definition_axis_orientation: MemberLoadAxisDefinitionAxisOrientation
    filling_height: float
    distance_from_member_end: bool
    load_is_over_total_length: bool
    has_force_eccentricity: bool
    eccentricity_horizontal_alignment: MemberLoadEccentricityHorizontalAlignment
    eccentricity_vertical_alignment: MemberLoadEccentricityVerticalAlignment
    eccentricity_section_middle: MemberLoadEccentricitySectionMiddle
    is_eccentricity_at_end_different_from_start: bool
    eccentricity_y_at_start: float
    eccentricity_z_at_start: float
    eccentricity_y_at_end: float
    eccentricity_z_at_end: float
    comment: str
    is_generated: bool
    generating_object_info: str
    form_finding_internal_force: MemberLoadFormFindingInternalForce
    form_finding_geometry_definition: MemberLoadFormFindingGeometryDefinition
    form_finding_force_definition: MemberLoadFormFindingForceDefinition
    form_finding_magnitude_is_defined_as_relative: bool
    form_finding_magnitude_absolute: float
    form_finding_magnitude_relative: float
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., load_type: _Optional[_Union[MemberLoadLoadType, str]] = ..., reference_to_list_of_members: bool = ..., members: _Optional[_Iterable[int]] = ..., load_case: _Optional[int] = ..., coordinate_system: _Optional[str] = ..., load_distribution: _Optional[_Union[MemberLoadLoadDistribution, str]] = ..., load_direction: _Optional[_Union[MemberLoadLoadDirection, str]] = ..., load_direction_orientation: _Optional[_Union[MemberLoadLoadDirectionOrientation, str]] = ..., form_finding_definition_type: _Optional[_Union[MemberLoadFormFindingDefinitionType, str]] = ..., magnitude: _Optional[float] = ..., magnitude_1: _Optional[float] = ..., magnitude_2: _Optional[float] = ..., magnitude_3: _Optional[float] = ..., magnitude_t_c: _Optional[float] = ..., magnitude_t_c_1: _Optional[float] = ..., magnitude_t_c_2: _Optional[float] = ..., magnitude_t_c_3: _Optional[float] = ..., magnitude_delta_t: _Optional[float] = ..., magnitude_delta_t_1: _Optional[float] = ..., magnitude_delta_t_2: _Optional[float] = ..., magnitude_delta_t_3: _Optional[float] = ..., magnitude_t_t: _Optional[float] = ..., magnitude_t_t_1: _Optional[float] = ..., magnitude_t_t_2: _Optional[float] = ..., magnitude_t_t_3: _Optional[float] = ..., magnitude_t_b: _Optional[float] = ..., magnitude_t_b_1: _Optional[float] = ..., magnitude_t_b_2: _Optional[float] = ..., magnitude_t_b_3: _Optional[float] = ..., individual_mass_components: bool = ..., mass_global: _Optional[float] = ..., mass_x: _Optional[float] = ..., mass_y: _Optional[float] = ..., mass_z: _Optional[float] = ..., distance_a_is_defined_as_relative: bool = ..., distance_a_absolute: _Optional[float] = ..., distance_a_relative: _Optional[float] = ..., distance_b_is_defined_as_relative: bool = ..., distance_b_absolute: _Optional[float] = ..., distance_b_relative: _Optional[float] = ..., distance_c_is_defined_as_relative: bool = ..., distance_c_absolute: _Optional[float] = ..., distance_c_relative: _Optional[float] = ..., count_n: _Optional[int] = ..., varying_load_parameters_are_defined_as_relative: bool = ..., varying_load_parameters: _Optional[_Union[MemberLoadVaryingLoadParametersTable, _Mapping]] = ..., varying_load_parameters_sorted: bool = ..., angular_velocity: _Optional[float] = ..., angular_acceleration: _Optional[float] = ..., axis_definition_type: _Optional[_Union[MemberLoadAxisDefinitionType, str]] = ..., axis_definition_p1: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., axis_definition_p1_x: _Optional[float] = ..., axis_definition_p1_y: _Optional[float] = ..., axis_definition_p1_z: _Optional[float] = ..., axis_definition_p2: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., axis_definition_p2_x: _Optional[float] = ..., axis_definition_p2_y: _Optional[float] = ..., axis_definition_p2_z: _Optional[float] = ..., axis_definition_axis: _Optional[_Union[MemberLoadAxisDefinitionAxis, str]] = ..., axis_definition_axis_orientation: _Optional[_Union[MemberLoadAxisDefinitionAxisOrientation, str]] = ..., filling_height: _Optional[float] = ..., distance_from_member_end: bool = ..., load_is_over_total_length: bool = ..., has_force_eccentricity: bool = ..., eccentricity_horizontal_alignment: _Optional[_Union[MemberLoadEccentricityHorizontalAlignment, str]] = ..., eccentricity_vertical_alignment: _Optional[_Union[MemberLoadEccentricityVerticalAlignment, str]] = ..., eccentricity_section_middle: _Optional[_Union[MemberLoadEccentricitySectionMiddle, str]] = ..., is_eccentricity_at_end_different_from_start: bool = ..., eccentricity_y_at_start: _Optional[float] = ..., eccentricity_z_at_start: _Optional[float] = ..., eccentricity_y_at_end: _Optional[float] = ..., eccentricity_z_at_end: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., form_finding_internal_force: _Optional[_Union[MemberLoadFormFindingInternalForce, str]] = ..., form_finding_geometry_definition: _Optional[_Union[MemberLoadFormFindingGeometryDefinition, str]] = ..., form_finding_force_definition: _Optional[_Union[MemberLoadFormFindingForceDefinition, str]] = ..., form_finding_magnitude_is_defined_as_relative: bool = ..., form_finding_magnitude_absolute: _Optional[float] = ..., form_finding_magnitude_relative: _Optional[float] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class MemberLoadVaryingLoadParametersTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[MemberLoadVaryingLoadParametersRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[MemberLoadVaryingLoadParametersRow, _Mapping]]] = ...) -> None: ...

class MemberLoadVaryingLoadParametersRow(_message.Message):
    __slots__ = ("no", "description", "distance", "delta_distance", "magnitude", "note", "magnitude_t_c", "magnitude_delta_t", "magnitude_t_t", "magnitude_t_b")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    DELTA_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_C_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_DELTA_T_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_T_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_B_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    distance: float
    delta_distance: float
    magnitude: float
    note: str
    magnitude_t_c: float
    magnitude_delta_t: float
    magnitude_t_t: float
    magnitude_t_b: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., distance: _Optional[float] = ..., delta_distance: _Optional[float] = ..., magnitude: _Optional[float] = ..., note: _Optional[str] = ..., magnitude_t_c: _Optional[float] = ..., magnitude_delta_t: _Optional[float] = ..., magnitude_t_t: _Optional[float] = ..., magnitude_t_b: _Optional[float] = ...) -> None: ...
