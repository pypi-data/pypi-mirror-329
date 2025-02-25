from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TimberEffectiveLengthsBucklingFactorValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_EFFECTIVE_LENGTHS_BUCKLING_FACTOR_VALUE_TYPE_THEORETICAL: _ClassVar[TimberEffectiveLengthsBucklingFactorValueType]
    TIMBER_EFFECTIVE_LENGTHS_BUCKLING_FACTOR_VALUE_TYPE_RECOMMENDED: _ClassVar[TimberEffectiveLengthsBucklingFactorValueType]

class TimberEffectiveLengthsNodalSupportsSupportType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_NONE: _ClassVar[TimberEffectiveLengthsNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_ALL: _ClassVar[TimberEffectiveLengthsNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y: _ClassVar[TimberEffectiveLengthsNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z: _ClassVar[TimberEffectiveLengthsNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_AND_TORSION: _ClassVar[TimberEffectiveLengthsNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_AND_TORSION_AND_WARPING: _ClassVar[TimberEffectiveLengthsNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION: _ClassVar[TimberEffectiveLengthsNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION_AND_WARPING: _ClassVar[TimberEffectiveLengthsNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_INDIVIDUALLY: _ClassVar[TimberEffectiveLengthsNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_RESTRAINT_ABOUT_X: _ClassVar[TimberEffectiveLengthsNodalSupportsSupportType]

class TimberEffectiveLengthsNodalSupportsEccentricityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_NONE: _ClassVar[TimberEffectiveLengthsNodalSupportsEccentricityType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_AT_LOWER_FLANGE: _ClassVar[TimberEffectiveLengthsNodalSupportsEccentricityType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_AT_UPPER_FLANGE: _ClassVar[TimberEffectiveLengthsNodalSupportsEccentricityType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_USER_VALUE: _ClassVar[TimberEffectiveLengthsNodalSupportsEccentricityType]

class TimberEffectiveLengthsNodalSupportsSupportInYType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_NO: _ClassVar[TimberEffectiveLengthsNodalSupportsSupportInYType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_SPRING: _ClassVar[TimberEffectiveLengthsNodalSupportsSupportInYType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_YES: _ClassVar[TimberEffectiveLengthsNodalSupportsSupportInYType]

class TimberEffectiveLengthsNodalSupportsRestraintAboutXType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_NO: _ClassVar[TimberEffectiveLengthsNodalSupportsRestraintAboutXType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_SPRING: _ClassVar[TimberEffectiveLengthsNodalSupportsRestraintAboutXType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_YES: _ClassVar[TimberEffectiveLengthsNodalSupportsRestraintAboutXType]

class TimberEffectiveLengthsNodalSupportsRestraintAboutZType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_NO: _ClassVar[TimberEffectiveLengthsNodalSupportsRestraintAboutZType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_SPRING: _ClassVar[TimberEffectiveLengthsNodalSupportsRestraintAboutZType]
    TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_YES: _ClassVar[TimberEffectiveLengthsNodalSupportsRestraintAboutZType]

class TimberEffectiveLengthsFireDesignNodalSupportsSupportType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_NONE: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_ALL: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_AND_TORSION: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_AND_TORSION_AND_WARPING: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION_AND_WARPING: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_INDIVIDUALLY: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsSupportType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_RESTRAINT_ABOUT_X: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsSupportType]

class TimberEffectiveLengthsFireDesignNodalSupportsEccentricityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_ECCENTRICITY_TYPE_NONE: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsEccentricityType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_ECCENTRICITY_TYPE_AT_LOWER_FLANGE: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsEccentricityType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_ECCENTRICITY_TYPE_AT_UPPER_FLANGE: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsEccentricityType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_ECCENTRICITY_TYPE_USER_VALUE: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsEccentricityType]

class TimberEffectiveLengthsFireDesignNodalSupportsSupportInYType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_NO: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsSupportInYType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_SPRING: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsSupportInYType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_YES: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsSupportInYType]

class TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutXType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_NO: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutXType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_SPRING: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutXType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_YES: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutXType]

class TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutZType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_NO: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutZType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_SPRING: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutZType]
    TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_YES: _ClassVar[TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutZType]

class TimberEffectiveLengthsDeterminationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_EFFECTIVE_LENGTHS_DETERMINATION_TYPE_ANALYTICAL: _ClassVar[TimberEffectiveLengthsDeterminationType]
    TIMBER_EFFECTIVE_LENGTHS_DETERMINATION_TYPE_EIGENVALUE_SOLVER: _ClassVar[TimberEffectiveLengthsDeterminationType]
    TIMBER_EFFECTIVE_LENGTHS_DETERMINATION_TYPE_USER_DEFINED: _ClassVar[TimberEffectiveLengthsDeterminationType]
TIMBER_EFFECTIVE_LENGTHS_BUCKLING_FACTOR_VALUE_TYPE_THEORETICAL: TimberEffectiveLengthsBucklingFactorValueType
TIMBER_EFFECTIVE_LENGTHS_BUCKLING_FACTOR_VALUE_TYPE_RECOMMENDED: TimberEffectiveLengthsBucklingFactorValueType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_NONE: TimberEffectiveLengthsNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_ALL: TimberEffectiveLengthsNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y: TimberEffectiveLengthsNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z: TimberEffectiveLengthsNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_AND_TORSION: TimberEffectiveLengthsNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_AND_TORSION_AND_WARPING: TimberEffectiveLengthsNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION: TimberEffectiveLengthsNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION_AND_WARPING: TimberEffectiveLengthsNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_INDIVIDUALLY: TimberEffectiveLengthsNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_RESTRAINT_ABOUT_X: TimberEffectiveLengthsNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_NONE: TimberEffectiveLengthsNodalSupportsEccentricityType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_AT_LOWER_FLANGE: TimberEffectiveLengthsNodalSupportsEccentricityType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_AT_UPPER_FLANGE: TimberEffectiveLengthsNodalSupportsEccentricityType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_USER_VALUE: TimberEffectiveLengthsNodalSupportsEccentricityType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_NO: TimberEffectiveLengthsNodalSupportsSupportInYType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_SPRING: TimberEffectiveLengthsNodalSupportsSupportInYType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_YES: TimberEffectiveLengthsNodalSupportsSupportInYType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_NO: TimberEffectiveLengthsNodalSupportsRestraintAboutXType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_SPRING: TimberEffectiveLengthsNodalSupportsRestraintAboutXType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_YES: TimberEffectiveLengthsNodalSupportsRestraintAboutXType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_NO: TimberEffectiveLengthsNodalSupportsRestraintAboutZType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_SPRING: TimberEffectiveLengthsNodalSupportsRestraintAboutZType
TIMBER_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_YES: TimberEffectiveLengthsNodalSupportsRestraintAboutZType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_NONE: TimberEffectiveLengthsFireDesignNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_ALL: TimberEffectiveLengthsFireDesignNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y: TimberEffectiveLengthsFireDesignNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z: TimberEffectiveLengthsFireDesignNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_AND_TORSION: TimberEffectiveLengthsFireDesignNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_AND_TORSION_AND_WARPING: TimberEffectiveLengthsFireDesignNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION: TimberEffectiveLengthsFireDesignNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION_AND_WARPING: TimberEffectiveLengthsFireDesignNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_INDIVIDUALLY: TimberEffectiveLengthsFireDesignNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_TYPE_RESTRAINT_ABOUT_X: TimberEffectiveLengthsFireDesignNodalSupportsSupportType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_ECCENTRICITY_TYPE_NONE: TimberEffectiveLengthsFireDesignNodalSupportsEccentricityType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_ECCENTRICITY_TYPE_AT_LOWER_FLANGE: TimberEffectiveLengthsFireDesignNodalSupportsEccentricityType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_ECCENTRICITY_TYPE_AT_UPPER_FLANGE: TimberEffectiveLengthsFireDesignNodalSupportsEccentricityType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_ECCENTRICITY_TYPE_USER_VALUE: TimberEffectiveLengthsFireDesignNodalSupportsEccentricityType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_NO: TimberEffectiveLengthsFireDesignNodalSupportsSupportInYType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_SPRING: TimberEffectiveLengthsFireDesignNodalSupportsSupportInYType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_YES: TimberEffectiveLengthsFireDesignNodalSupportsSupportInYType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_NO: TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutXType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_SPRING: TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutXType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_YES: TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutXType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_NO: TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutZType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_SPRING: TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutZType
TIMBER_EFFECTIVE_LENGTHS_FIRE_DESIGN_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_YES: TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutZType
TIMBER_EFFECTIVE_LENGTHS_DETERMINATION_TYPE_ANALYTICAL: TimberEffectiveLengthsDeterminationType
TIMBER_EFFECTIVE_LENGTHS_DETERMINATION_TYPE_EIGENVALUE_SOLVER: TimberEffectiveLengthsDeterminationType
TIMBER_EFFECTIVE_LENGTHS_DETERMINATION_TYPE_USER_DEFINED: TimberEffectiveLengthsDeterminationType

class TimberEffectiveLengths(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "comment", "members", "member_sets", "flexural_buckling_about_y", "flexural_buckling_about_z", "lateral_torsional_buckling", "buckling_factor_value_type", "is_generated", "generating_object_info", "intermediate_nodes", "different_properties", "factors_definition_absolute", "nodal_supports", "factors", "lengths", "fire_design_nodal_supports", "fire_design_factors", "fire_design_lengths", "fire_design_intermediate_nodes", "fire_design_different_properties", "fire_design_factors_definition_absolute", "fire_design_different_buckling_factors", "import_from_stability_analysis_enabled", "stability_import_data_factors_definition_absolute", "stability_import_data_member_y", "stability_import_data_loading_y", "stability_import_data_mode_number_y", "stability_import_data_member_z", "stability_import_data_loading_z", "stability_import_data_mode_number_z", "stability_import_data_factors", "stability_import_data_lengths", "stability_import_data_user_defined_y", "stability_import_data_user_defined_z", "determination_type", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_ABOUT_Y_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_FIELD_NUMBER: _ClassVar[int]
    BUCKLING_FACTOR_VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    INTERMEDIATE_NODES_FIELD_NUMBER: _ClassVar[int]
    DIFFERENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    FACTORS_DEFINITION_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    NODAL_SUPPORTS_FIELD_NUMBER: _ClassVar[int]
    FACTORS_FIELD_NUMBER: _ClassVar[int]
    LENGTHS_FIELD_NUMBER: _ClassVar[int]
    FIRE_DESIGN_NODAL_SUPPORTS_FIELD_NUMBER: _ClassVar[int]
    FIRE_DESIGN_FACTORS_FIELD_NUMBER: _ClassVar[int]
    FIRE_DESIGN_LENGTHS_FIELD_NUMBER: _ClassVar[int]
    FIRE_DESIGN_INTERMEDIATE_NODES_FIELD_NUMBER: _ClassVar[int]
    FIRE_DESIGN_DIFFERENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    FIRE_DESIGN_FACTORS_DEFINITION_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    FIRE_DESIGN_DIFFERENT_BUCKLING_FACTORS_FIELD_NUMBER: _ClassVar[int]
    IMPORT_FROM_STABILITY_ANALYSIS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    STABILITY_IMPORT_DATA_FACTORS_DEFINITION_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    STABILITY_IMPORT_DATA_MEMBER_Y_FIELD_NUMBER: _ClassVar[int]
    STABILITY_IMPORT_DATA_LOADING_Y_FIELD_NUMBER: _ClassVar[int]
    STABILITY_IMPORT_DATA_MODE_NUMBER_Y_FIELD_NUMBER: _ClassVar[int]
    STABILITY_IMPORT_DATA_MEMBER_Z_FIELD_NUMBER: _ClassVar[int]
    STABILITY_IMPORT_DATA_LOADING_Z_FIELD_NUMBER: _ClassVar[int]
    STABILITY_IMPORT_DATA_MODE_NUMBER_Z_FIELD_NUMBER: _ClassVar[int]
    STABILITY_IMPORT_DATA_FACTORS_FIELD_NUMBER: _ClassVar[int]
    STABILITY_IMPORT_DATA_LENGTHS_FIELD_NUMBER: _ClassVar[int]
    STABILITY_IMPORT_DATA_USER_DEFINED_Y_FIELD_NUMBER: _ClassVar[int]
    STABILITY_IMPORT_DATA_USER_DEFINED_Z_FIELD_NUMBER: _ClassVar[int]
    DETERMINATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    comment: str
    members: _containers.RepeatedScalarFieldContainer[int]
    member_sets: _containers.RepeatedScalarFieldContainer[int]
    flexural_buckling_about_y: bool
    flexural_buckling_about_z: bool
    lateral_torsional_buckling: bool
    buckling_factor_value_type: TimberEffectiveLengthsBucklingFactorValueType
    is_generated: bool
    generating_object_info: str
    intermediate_nodes: bool
    different_properties: bool
    factors_definition_absolute: bool
    nodal_supports: TimberEffectiveLengthsNodalSupportsTable
    factors: TimberEffectiveLengthsFactorsTable
    lengths: TimberEffectiveLengthsLengthsTable
    fire_design_nodal_supports: TimberEffectiveLengthsFireDesignNodalSupportsTable
    fire_design_factors: TimberEffectiveLengthsFireDesignFactorsTable
    fire_design_lengths: TimberEffectiveLengthsFireDesignLengthsTable
    fire_design_intermediate_nodes: bool
    fire_design_different_properties: bool
    fire_design_factors_definition_absolute: bool
    fire_design_different_buckling_factors: bool
    import_from_stability_analysis_enabled: bool
    stability_import_data_factors_definition_absolute: bool
    stability_import_data_member_y: int
    stability_import_data_loading_y: int
    stability_import_data_mode_number_y: int
    stability_import_data_member_z: int
    stability_import_data_loading_z: int
    stability_import_data_mode_number_z: int
    stability_import_data_factors: TimberEffectiveLengthsStabilityImportDataFactorsTable
    stability_import_data_lengths: TimberEffectiveLengthsStabilityImportDataLengthsTable
    stability_import_data_user_defined_y: bool
    stability_import_data_user_defined_z: bool
    determination_type: TimberEffectiveLengthsDeterminationType
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., comment: _Optional[str] = ..., members: _Optional[_Iterable[int]] = ..., member_sets: _Optional[_Iterable[int]] = ..., flexural_buckling_about_y: bool = ..., flexural_buckling_about_z: bool = ..., lateral_torsional_buckling: bool = ..., buckling_factor_value_type: _Optional[_Union[TimberEffectiveLengthsBucklingFactorValueType, str]] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., intermediate_nodes: bool = ..., different_properties: bool = ..., factors_definition_absolute: bool = ..., nodal_supports: _Optional[_Union[TimberEffectiveLengthsNodalSupportsTable, _Mapping]] = ..., factors: _Optional[_Union[TimberEffectiveLengthsFactorsTable, _Mapping]] = ..., lengths: _Optional[_Union[TimberEffectiveLengthsLengthsTable, _Mapping]] = ..., fire_design_nodal_supports: _Optional[_Union[TimberEffectiveLengthsFireDesignNodalSupportsTable, _Mapping]] = ..., fire_design_factors: _Optional[_Union[TimberEffectiveLengthsFireDesignFactorsTable, _Mapping]] = ..., fire_design_lengths: _Optional[_Union[TimberEffectiveLengthsFireDesignLengthsTable, _Mapping]] = ..., fire_design_intermediate_nodes: bool = ..., fire_design_different_properties: bool = ..., fire_design_factors_definition_absolute: bool = ..., fire_design_different_buckling_factors: bool = ..., import_from_stability_analysis_enabled: bool = ..., stability_import_data_factors_definition_absolute: bool = ..., stability_import_data_member_y: _Optional[int] = ..., stability_import_data_loading_y: _Optional[int] = ..., stability_import_data_mode_number_y: _Optional[int] = ..., stability_import_data_member_z: _Optional[int] = ..., stability_import_data_loading_z: _Optional[int] = ..., stability_import_data_mode_number_z: _Optional[int] = ..., stability_import_data_factors: _Optional[_Union[TimberEffectiveLengthsStabilityImportDataFactorsTable, _Mapping]] = ..., stability_import_data_lengths: _Optional[_Union[TimberEffectiveLengthsStabilityImportDataLengthsTable, _Mapping]] = ..., stability_import_data_user_defined_y: bool = ..., stability_import_data_user_defined_z: bool = ..., determination_type: _Optional[_Union[TimberEffectiveLengthsDeterminationType, str]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class TimberEffectiveLengthsNodalSupportsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[TimberEffectiveLengthsNodalSupportsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[TimberEffectiveLengthsNodalSupportsRow, _Mapping]]] = ...) -> None: ...

class TimberEffectiveLengthsNodalSupportsRow(_message.Message):
    __slots__ = ("no", "description", "support_type", "support_in_z", "support_spring_in_y", "eccentricity_type", "eccentricity_ez", "restraint_spring_about_x", "restraint_spring_about_z", "support_in_y_type", "restraint_about_x_type", "restraint_about_z_type", "nodes")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_IN_Z_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_SPRING_IN_Y_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_EZ_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_SPRING_ABOUT_X_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_SPRING_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_IN_Y_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_ABOUT_X_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_ABOUT_Z_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    support_type: TimberEffectiveLengthsNodalSupportsSupportType
    support_in_z: bool
    support_spring_in_y: float
    eccentricity_type: TimberEffectiveLengthsNodalSupportsEccentricityType
    eccentricity_ez: float
    restraint_spring_about_x: float
    restraint_spring_about_z: float
    support_in_y_type: TimberEffectiveLengthsNodalSupportsSupportInYType
    restraint_about_x_type: TimberEffectiveLengthsNodalSupportsRestraintAboutXType
    restraint_about_z_type: TimberEffectiveLengthsNodalSupportsRestraintAboutZType
    nodes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., support_type: _Optional[_Union[TimberEffectiveLengthsNodalSupportsSupportType, str]] = ..., support_in_z: bool = ..., support_spring_in_y: _Optional[float] = ..., eccentricity_type: _Optional[_Union[TimberEffectiveLengthsNodalSupportsEccentricityType, str]] = ..., eccentricity_ez: _Optional[float] = ..., restraint_spring_about_x: _Optional[float] = ..., restraint_spring_about_z: _Optional[float] = ..., support_in_y_type: _Optional[_Union[TimberEffectiveLengthsNodalSupportsSupportInYType, str]] = ..., restraint_about_x_type: _Optional[_Union[TimberEffectiveLengthsNodalSupportsRestraintAboutXType, str]] = ..., restraint_about_z_type: _Optional[_Union[TimberEffectiveLengthsNodalSupportsRestraintAboutZType, str]] = ..., nodes: _Optional[_Iterable[int]] = ...) -> None: ...

class TimberEffectiveLengthsFactorsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[TimberEffectiveLengthsFactorsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[TimberEffectiveLengthsFactorsRow, _Mapping]]] = ...) -> None: ...

class TimberEffectiveLengthsFactorsRow(_message.Message):
    __slots__ = ("no", "description", "flexural_buckling_u", "flexural_buckling_v", "lateral_torsional_buckling", "lateral_torsional_buckling_top", "lateral_torsional_buckling_bottom", "critical_moment")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_U_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_V_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_TOP_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_MOMENT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    flexural_buckling_u: float
    flexural_buckling_v: float
    lateral_torsional_buckling: float
    lateral_torsional_buckling_top: float
    lateral_torsional_buckling_bottom: float
    critical_moment: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., flexural_buckling_u: _Optional[float] = ..., flexural_buckling_v: _Optional[float] = ..., lateral_torsional_buckling: _Optional[float] = ..., lateral_torsional_buckling_top: _Optional[float] = ..., lateral_torsional_buckling_bottom: _Optional[float] = ..., critical_moment: _Optional[float] = ...) -> None: ...

class TimberEffectiveLengthsLengthsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[TimberEffectiveLengthsLengthsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[TimberEffectiveLengthsLengthsRow, _Mapping]]] = ...) -> None: ...

class TimberEffectiveLengthsLengthsRow(_message.Message):
    __slots__ = ("no", "description", "flexural_buckling_u", "flexural_buckling_v", "lateral_torsional_buckling", "lateral_torsional_buckling_top", "lateral_torsional_buckling_bottom", "critical_moment")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_U_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_V_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_TOP_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_MOMENT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    flexural_buckling_u: float
    flexural_buckling_v: float
    lateral_torsional_buckling: float
    lateral_torsional_buckling_top: float
    lateral_torsional_buckling_bottom: float
    critical_moment: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., flexural_buckling_u: _Optional[float] = ..., flexural_buckling_v: _Optional[float] = ..., lateral_torsional_buckling: _Optional[float] = ..., lateral_torsional_buckling_top: _Optional[float] = ..., lateral_torsional_buckling_bottom: _Optional[float] = ..., critical_moment: _Optional[float] = ...) -> None: ...

class TimberEffectiveLengthsFireDesignNodalSupportsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[TimberEffectiveLengthsFireDesignNodalSupportsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[TimberEffectiveLengthsFireDesignNodalSupportsRow, _Mapping]]] = ...) -> None: ...

class TimberEffectiveLengthsFireDesignNodalSupportsRow(_message.Message):
    __slots__ = ("no", "description", "support_type", "support_in_z", "support_spring_in_y", "eccentricity_type", "eccentricity_ez", "restraint_spring_about_x", "restraint_spring_about_z", "support_in_y_type", "restraint_about_x_type", "restraint_about_z_type", "nodes")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_IN_Z_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_SPRING_IN_Y_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_EZ_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_SPRING_ABOUT_X_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_SPRING_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_IN_Y_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_ABOUT_X_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_ABOUT_Z_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    support_type: TimberEffectiveLengthsFireDesignNodalSupportsSupportType
    support_in_z: bool
    support_spring_in_y: float
    eccentricity_type: TimberEffectiveLengthsFireDesignNodalSupportsEccentricityType
    eccentricity_ez: float
    restraint_spring_about_x: float
    restraint_spring_about_z: float
    support_in_y_type: TimberEffectiveLengthsFireDesignNodalSupportsSupportInYType
    restraint_about_x_type: TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutXType
    restraint_about_z_type: TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutZType
    nodes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., support_type: _Optional[_Union[TimberEffectiveLengthsFireDesignNodalSupportsSupportType, str]] = ..., support_in_z: bool = ..., support_spring_in_y: _Optional[float] = ..., eccentricity_type: _Optional[_Union[TimberEffectiveLengthsFireDesignNodalSupportsEccentricityType, str]] = ..., eccentricity_ez: _Optional[float] = ..., restraint_spring_about_x: _Optional[float] = ..., restraint_spring_about_z: _Optional[float] = ..., support_in_y_type: _Optional[_Union[TimberEffectiveLengthsFireDesignNodalSupportsSupportInYType, str]] = ..., restraint_about_x_type: _Optional[_Union[TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutXType, str]] = ..., restraint_about_z_type: _Optional[_Union[TimberEffectiveLengthsFireDesignNodalSupportsRestraintAboutZType, str]] = ..., nodes: _Optional[_Iterable[int]] = ...) -> None: ...

class TimberEffectiveLengthsFireDesignFactorsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[TimberEffectiveLengthsFireDesignFactorsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[TimberEffectiveLengthsFireDesignFactorsRow, _Mapping]]] = ...) -> None: ...

class TimberEffectiveLengthsFireDesignFactorsRow(_message.Message):
    __slots__ = ("no", "description", "flexural_buckling_u", "flexural_buckling_v", "lateral_torsional_buckling", "lateral_torsional_buckling_top", "lateral_torsional_buckling_bottom", "critical_moment")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_U_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_V_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_TOP_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_MOMENT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    flexural_buckling_u: float
    flexural_buckling_v: float
    lateral_torsional_buckling: float
    lateral_torsional_buckling_top: float
    lateral_torsional_buckling_bottom: float
    critical_moment: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., flexural_buckling_u: _Optional[float] = ..., flexural_buckling_v: _Optional[float] = ..., lateral_torsional_buckling: _Optional[float] = ..., lateral_torsional_buckling_top: _Optional[float] = ..., lateral_torsional_buckling_bottom: _Optional[float] = ..., critical_moment: _Optional[float] = ...) -> None: ...

class TimberEffectiveLengthsFireDesignLengthsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[TimberEffectiveLengthsFireDesignLengthsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[TimberEffectiveLengthsFireDesignLengthsRow, _Mapping]]] = ...) -> None: ...

class TimberEffectiveLengthsFireDesignLengthsRow(_message.Message):
    __slots__ = ("no", "description", "flexural_buckling_u", "flexural_buckling_v", "lateral_torsional_buckling", "lateral_torsional_buckling_top", "lateral_torsional_buckling_bottom", "critical_moment")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_U_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_V_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_TOP_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_MOMENT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    flexural_buckling_u: float
    flexural_buckling_v: float
    lateral_torsional_buckling: float
    lateral_torsional_buckling_top: float
    lateral_torsional_buckling_bottom: float
    critical_moment: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., flexural_buckling_u: _Optional[float] = ..., flexural_buckling_v: _Optional[float] = ..., lateral_torsional_buckling: _Optional[float] = ..., lateral_torsional_buckling_top: _Optional[float] = ..., lateral_torsional_buckling_bottom: _Optional[float] = ..., critical_moment: _Optional[float] = ...) -> None: ...

class TimberEffectiveLengthsStabilityImportDataFactorsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[TimberEffectiveLengthsStabilityImportDataFactorsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[TimberEffectiveLengthsStabilityImportDataFactorsRow, _Mapping]]] = ...) -> None: ...

class TimberEffectiveLengthsStabilityImportDataFactorsRow(_message.Message):
    __slots__ = ("no", "description", "flexural_buckling_u", "flexural_buckling_v")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_U_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_V_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    flexural_buckling_u: float
    flexural_buckling_v: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., flexural_buckling_u: _Optional[float] = ..., flexural_buckling_v: _Optional[float] = ...) -> None: ...

class TimberEffectiveLengthsStabilityImportDataLengthsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[TimberEffectiveLengthsStabilityImportDataLengthsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[TimberEffectiveLengthsStabilityImportDataLengthsRow, _Mapping]]] = ...) -> None: ...

class TimberEffectiveLengthsStabilityImportDataLengthsRow(_message.Message):
    __slots__ = ("no", "description", "flexural_buckling_u", "flexural_buckling_v")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_U_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_V_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    flexural_buckling_u: float
    flexural_buckling_v: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., flexural_buckling_u: _Optional[float] = ..., flexural_buckling_v: _Optional[float] = ...) -> None: ...
