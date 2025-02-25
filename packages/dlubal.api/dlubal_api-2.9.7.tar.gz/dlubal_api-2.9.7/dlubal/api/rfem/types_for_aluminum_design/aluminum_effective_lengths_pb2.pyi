from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AluminumEffectiveLengthsBucklingFactorValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_EFFECTIVE_LENGTHS_BUCKLING_FACTOR_VALUE_TYPE_THEORETICAL: _ClassVar[AluminumEffectiveLengthsBucklingFactorValueType]
    ALUMINUM_EFFECTIVE_LENGTHS_BUCKLING_FACTOR_VALUE_TYPE_RECOMMENDED: _ClassVar[AluminumEffectiveLengthsBucklingFactorValueType]

class AluminumEffectiveLengthsDeterminationMcrEurope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_MCR_EUROPE_EIGENVALUE: _ClassVar[AluminumEffectiveLengthsDeterminationMcrEurope]
    ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_MCR_EUROPE_USER_DEFINED: _ClassVar[AluminumEffectiveLengthsDeterminationMcrEurope]

class AluminumEffectiveLengthsDeterminationMeAdm(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_ME_ADM_EIGENVALUE_METHOD: _ClassVar[AluminumEffectiveLengthsDeterminationMeAdm]
    ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_ME_ADM_ACC_TO_CHAPTER_F: _ClassVar[AluminumEffectiveLengthsDeterminationMeAdm]
    ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_ME_ADM_USER_DEFINED: _ClassVar[AluminumEffectiveLengthsDeterminationMeAdm]

class AluminumEffectiveLengthsDeterminationCbAdm(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_CB_ADM_BASIC_VALUE: _ClassVar[AluminumEffectiveLengthsDeterminationCbAdm]
    ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_CB_ADM_AUTOMATICALLY_ACC_TO_F_4_1: _ClassVar[AluminumEffectiveLengthsDeterminationCbAdm]
    ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_CB_ADM_USER_DEFINED: _ClassVar[AluminumEffectiveLengthsDeterminationCbAdm]

class AluminumEffectiveLengthsDeterminationCbMemberTypeAdm(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_CB_MEMBER_TYPE_ADM_BEAM: _ClassVar[AluminumEffectiveLengthsDeterminationCbMemberTypeAdm]
    ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_CB_MEMBER_TYPE_ADM_CANTILEVER: _ClassVar[AluminumEffectiveLengthsDeterminationCbMemberTypeAdm]

class AluminumEffectiveLengthsNodalSupportsSupportType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_NONE: _ClassVar[AluminumEffectiveLengthsNodalSupportsSupportType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_ALL: _ClassVar[AluminumEffectiveLengthsNodalSupportsSupportType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y: _ClassVar[AluminumEffectiveLengthsNodalSupportsSupportType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z: _ClassVar[AluminumEffectiveLengthsNodalSupportsSupportType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_AND_TORSION: _ClassVar[AluminumEffectiveLengthsNodalSupportsSupportType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_AND_TORSION_AND_WARPING: _ClassVar[AluminumEffectiveLengthsNodalSupportsSupportType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION: _ClassVar[AluminumEffectiveLengthsNodalSupportsSupportType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION_AND_WARPING: _ClassVar[AluminumEffectiveLengthsNodalSupportsSupportType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_INDIVIDUALLY: _ClassVar[AluminumEffectiveLengthsNodalSupportsSupportType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_RESTRAINT_ABOUT_X: _ClassVar[AluminumEffectiveLengthsNodalSupportsSupportType]

class AluminumEffectiveLengthsNodalSupportsEccentricityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_NONE: _ClassVar[AluminumEffectiveLengthsNodalSupportsEccentricityType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_AT_LOWER_FLANGE: _ClassVar[AluminumEffectiveLengthsNodalSupportsEccentricityType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_AT_UPPER_FLANGE: _ClassVar[AluminumEffectiveLengthsNodalSupportsEccentricityType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_USER_VALUE: _ClassVar[AluminumEffectiveLengthsNodalSupportsEccentricityType]

class AluminumEffectiveLengthsNodalSupportsSupportInYType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_NO: _ClassVar[AluminumEffectiveLengthsNodalSupportsSupportInYType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_SPRING: _ClassVar[AluminumEffectiveLengthsNodalSupportsSupportInYType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_YES: _ClassVar[AluminumEffectiveLengthsNodalSupportsSupportInYType]

class AluminumEffectiveLengthsNodalSupportsRestraintAboutXType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_NO: _ClassVar[AluminumEffectiveLengthsNodalSupportsRestraintAboutXType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_SPRING: _ClassVar[AluminumEffectiveLengthsNodalSupportsRestraintAboutXType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_YES: _ClassVar[AluminumEffectiveLengthsNodalSupportsRestraintAboutXType]

class AluminumEffectiveLengthsNodalSupportsRestraintAboutZType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_NO: _ClassVar[AluminumEffectiveLengthsNodalSupportsRestraintAboutZType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_SPRING: _ClassVar[AluminumEffectiveLengthsNodalSupportsRestraintAboutZType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_YES: _ClassVar[AluminumEffectiveLengthsNodalSupportsRestraintAboutZType]

class AluminumEffectiveLengthsNodalSupportsRestraintWarpingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_WARPING_TYPE_SUPPORT_STATUS_NO: _ClassVar[AluminumEffectiveLengthsNodalSupportsRestraintWarpingType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_WARPING_TYPE_SUPPORT_STATUS_SPRING: _ClassVar[AluminumEffectiveLengthsNodalSupportsRestraintWarpingType]
    ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_WARPING_TYPE_SUPPORT_STATUS_YES: _ClassVar[AluminumEffectiveLengthsNodalSupportsRestraintWarpingType]
ALUMINUM_EFFECTIVE_LENGTHS_BUCKLING_FACTOR_VALUE_TYPE_THEORETICAL: AluminumEffectiveLengthsBucklingFactorValueType
ALUMINUM_EFFECTIVE_LENGTHS_BUCKLING_FACTOR_VALUE_TYPE_RECOMMENDED: AluminumEffectiveLengthsBucklingFactorValueType
ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_MCR_EUROPE_EIGENVALUE: AluminumEffectiveLengthsDeterminationMcrEurope
ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_MCR_EUROPE_USER_DEFINED: AluminumEffectiveLengthsDeterminationMcrEurope
ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_ME_ADM_EIGENVALUE_METHOD: AluminumEffectiveLengthsDeterminationMeAdm
ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_ME_ADM_ACC_TO_CHAPTER_F: AluminumEffectiveLengthsDeterminationMeAdm
ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_ME_ADM_USER_DEFINED: AluminumEffectiveLengthsDeterminationMeAdm
ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_CB_ADM_BASIC_VALUE: AluminumEffectiveLengthsDeterminationCbAdm
ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_CB_ADM_AUTOMATICALLY_ACC_TO_F_4_1: AluminumEffectiveLengthsDeterminationCbAdm
ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_CB_ADM_USER_DEFINED: AluminumEffectiveLengthsDeterminationCbAdm
ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_CB_MEMBER_TYPE_ADM_BEAM: AluminumEffectiveLengthsDeterminationCbMemberTypeAdm
ALUMINUM_EFFECTIVE_LENGTHS_DETERMINATION_CB_MEMBER_TYPE_ADM_CANTILEVER: AluminumEffectiveLengthsDeterminationCbMemberTypeAdm
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_NONE: AluminumEffectiveLengthsNodalSupportsSupportType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_ALL: AluminumEffectiveLengthsNodalSupportsSupportType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Y: AluminumEffectiveLengthsNodalSupportsSupportType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z: AluminumEffectiveLengthsNodalSupportsSupportType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_AND_TORSION: AluminumEffectiveLengthsNodalSupportsSupportType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_AND_TORSION_AND_WARPING: AluminumEffectiveLengthsNodalSupportsSupportType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION: AluminumEffectiveLengthsNodalSupportsSupportType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_FIXED_IN_Z_Y_AND_TORSION_AND_WARPING: AluminumEffectiveLengthsNodalSupportsSupportType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_INDIVIDUALLY: AluminumEffectiveLengthsNodalSupportsSupportType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_TYPE_RESTRAINT_ABOUT_X: AluminumEffectiveLengthsNodalSupportsSupportType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_NONE: AluminumEffectiveLengthsNodalSupportsEccentricityType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_AT_LOWER_FLANGE: AluminumEffectiveLengthsNodalSupportsEccentricityType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_AT_UPPER_FLANGE: AluminumEffectiveLengthsNodalSupportsEccentricityType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_ECCENTRICITY_TYPE_USER_VALUE: AluminumEffectiveLengthsNodalSupportsEccentricityType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_NO: AluminumEffectiveLengthsNodalSupportsSupportInYType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_SPRING: AluminumEffectiveLengthsNodalSupportsSupportInYType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_SUPPORT_IN_Y_TYPE_SUPPORT_STATUS_YES: AluminumEffectiveLengthsNodalSupportsSupportInYType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_NO: AluminumEffectiveLengthsNodalSupportsRestraintAboutXType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_SPRING: AluminumEffectiveLengthsNodalSupportsRestraintAboutXType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_X_TYPE_SUPPORT_STATUS_YES: AluminumEffectiveLengthsNodalSupportsRestraintAboutXType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_NO: AluminumEffectiveLengthsNodalSupportsRestraintAboutZType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_SPRING: AluminumEffectiveLengthsNodalSupportsRestraintAboutZType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_ABOUT_Z_TYPE_SUPPORT_STATUS_YES: AluminumEffectiveLengthsNodalSupportsRestraintAboutZType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_WARPING_TYPE_SUPPORT_STATUS_NO: AluminumEffectiveLengthsNodalSupportsRestraintWarpingType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_WARPING_TYPE_SUPPORT_STATUS_SPRING: AluminumEffectiveLengthsNodalSupportsRestraintWarpingType
ALUMINUM_EFFECTIVE_LENGTHS_NODAL_SUPPORTS_RESTRAINT_WARPING_TYPE_SUPPORT_STATUS_YES: AluminumEffectiveLengthsNodalSupportsRestraintWarpingType

class AluminumEffectiveLengths(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "comment", "members", "member_sets", "flexural_buckling_about_y", "flexural_buckling_about_z", "torsional_buckling", "lateral_torsional_buckling", "buckling_factor_value_type", "principal_section_axes", "geometric_section_axes", "is_generated", "generating_object_info", "factors_definition_absolute", "intermediate_nodes", "different_properties", "determination_mcr_europe", "determination_me_adm", "determination_cb_adm", "cb_factor_adm", "determination_cb_member_type_adm", "nodal_supports", "factors", "lengths", "import_from_stability_analysis_enabled", "stability_import_data_factors_definition_absolute", "stability_import_data_member_y", "stability_import_data_loading_y", "stability_import_data_mode_number_y", "stability_import_data_member_z", "stability_import_data_loading_z", "stability_import_data_mode_number_z", "stability_import_data_factors", "stability_import_data_lengths", "stability_import_data_user_defined_y", "stability_import_data_user_defined_z", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_ABOUT_Y_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
    TORSIONAL_BUCKLING_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_FIELD_NUMBER: _ClassVar[int]
    BUCKLING_FACTOR_VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PRINCIPAL_SECTION_AXES_FIELD_NUMBER: _ClassVar[int]
    GEOMETRIC_SECTION_AXES_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    FACTORS_DEFINITION_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    INTERMEDIATE_NODES_FIELD_NUMBER: _ClassVar[int]
    DIFFERENT_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    DETERMINATION_MCR_EUROPE_FIELD_NUMBER: _ClassVar[int]
    DETERMINATION_ME_ADM_FIELD_NUMBER: _ClassVar[int]
    DETERMINATION_CB_ADM_FIELD_NUMBER: _ClassVar[int]
    CB_FACTOR_ADM_FIELD_NUMBER: _ClassVar[int]
    DETERMINATION_CB_MEMBER_TYPE_ADM_FIELD_NUMBER: _ClassVar[int]
    NODAL_SUPPORTS_FIELD_NUMBER: _ClassVar[int]
    FACTORS_FIELD_NUMBER: _ClassVar[int]
    LENGTHS_FIELD_NUMBER: _ClassVar[int]
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
    torsional_buckling: bool
    lateral_torsional_buckling: bool
    buckling_factor_value_type: AluminumEffectiveLengthsBucklingFactorValueType
    principal_section_axes: bool
    geometric_section_axes: bool
    is_generated: bool
    generating_object_info: str
    factors_definition_absolute: bool
    intermediate_nodes: bool
    different_properties: bool
    determination_mcr_europe: AluminumEffectiveLengthsDeterminationMcrEurope
    determination_me_adm: AluminumEffectiveLengthsDeterminationMeAdm
    determination_cb_adm: AluminumEffectiveLengthsDeterminationCbAdm
    cb_factor_adm: float
    determination_cb_member_type_adm: AluminumEffectiveLengthsDeterminationCbMemberTypeAdm
    nodal_supports: AluminumEffectiveLengthsNodalSupportsTable
    factors: AluminumEffectiveLengthsFactorsTable
    lengths: AluminumEffectiveLengthsLengthsTable
    import_from_stability_analysis_enabled: bool
    stability_import_data_factors_definition_absolute: bool
    stability_import_data_member_y: int
    stability_import_data_loading_y: int
    stability_import_data_mode_number_y: int
    stability_import_data_member_z: int
    stability_import_data_loading_z: int
    stability_import_data_mode_number_z: int
    stability_import_data_factors: AluminumEffectiveLengthsStabilityImportDataFactorsTable
    stability_import_data_lengths: AluminumEffectiveLengthsStabilityImportDataLengthsTable
    stability_import_data_user_defined_y: bool
    stability_import_data_user_defined_z: bool
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., comment: _Optional[str] = ..., members: _Optional[_Iterable[int]] = ..., member_sets: _Optional[_Iterable[int]] = ..., flexural_buckling_about_y: bool = ..., flexural_buckling_about_z: bool = ..., torsional_buckling: bool = ..., lateral_torsional_buckling: bool = ..., buckling_factor_value_type: _Optional[_Union[AluminumEffectiveLengthsBucklingFactorValueType, str]] = ..., principal_section_axes: bool = ..., geometric_section_axes: bool = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., factors_definition_absolute: bool = ..., intermediate_nodes: bool = ..., different_properties: bool = ..., determination_mcr_europe: _Optional[_Union[AluminumEffectiveLengthsDeterminationMcrEurope, str]] = ..., determination_me_adm: _Optional[_Union[AluminumEffectiveLengthsDeterminationMeAdm, str]] = ..., determination_cb_adm: _Optional[_Union[AluminumEffectiveLengthsDeterminationCbAdm, str]] = ..., cb_factor_adm: _Optional[float] = ..., determination_cb_member_type_adm: _Optional[_Union[AluminumEffectiveLengthsDeterminationCbMemberTypeAdm, str]] = ..., nodal_supports: _Optional[_Union[AluminumEffectiveLengthsNodalSupportsTable, _Mapping]] = ..., factors: _Optional[_Union[AluminumEffectiveLengthsFactorsTable, _Mapping]] = ..., lengths: _Optional[_Union[AluminumEffectiveLengthsLengthsTable, _Mapping]] = ..., import_from_stability_analysis_enabled: bool = ..., stability_import_data_factors_definition_absolute: bool = ..., stability_import_data_member_y: _Optional[int] = ..., stability_import_data_loading_y: _Optional[int] = ..., stability_import_data_mode_number_y: _Optional[int] = ..., stability_import_data_member_z: _Optional[int] = ..., stability_import_data_loading_z: _Optional[int] = ..., stability_import_data_mode_number_z: _Optional[int] = ..., stability_import_data_factors: _Optional[_Union[AluminumEffectiveLengthsStabilityImportDataFactorsTable, _Mapping]] = ..., stability_import_data_lengths: _Optional[_Union[AluminumEffectiveLengthsStabilityImportDataLengthsTable, _Mapping]] = ..., stability_import_data_user_defined_y: bool = ..., stability_import_data_user_defined_z: bool = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class AluminumEffectiveLengthsNodalSupportsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[AluminumEffectiveLengthsNodalSupportsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[AluminumEffectiveLengthsNodalSupportsRow, _Mapping]]] = ...) -> None: ...

class AluminumEffectiveLengthsNodalSupportsRow(_message.Message):
    __slots__ = ("no", "description", "support_type", "support_in_z", "support_spring_in_y", "eccentricity_type", "eccentricity_ez", "restraint_spring_about_x", "restraint_spring_about_z", "restraint_spring_warping", "support_in_y_type", "restraint_about_x_type", "restraint_about_z_type", "restraint_warping_type", "nodes")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_IN_Z_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_SPRING_IN_Y_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_EZ_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_SPRING_ABOUT_X_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_SPRING_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_SPRING_WARPING_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_IN_Y_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_ABOUT_X_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_ABOUT_Z_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESTRAINT_WARPING_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    support_type: AluminumEffectiveLengthsNodalSupportsSupportType
    support_in_z: bool
    support_spring_in_y: float
    eccentricity_type: AluminumEffectiveLengthsNodalSupportsEccentricityType
    eccentricity_ez: float
    restraint_spring_about_x: float
    restraint_spring_about_z: float
    restraint_spring_warping: float
    support_in_y_type: AluminumEffectiveLengthsNodalSupportsSupportInYType
    restraint_about_x_type: AluminumEffectiveLengthsNodalSupportsRestraintAboutXType
    restraint_about_z_type: AluminumEffectiveLengthsNodalSupportsRestraintAboutZType
    restraint_warping_type: AluminumEffectiveLengthsNodalSupportsRestraintWarpingType
    nodes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., support_type: _Optional[_Union[AluminumEffectiveLengthsNodalSupportsSupportType, str]] = ..., support_in_z: bool = ..., support_spring_in_y: _Optional[float] = ..., eccentricity_type: _Optional[_Union[AluminumEffectiveLengthsNodalSupportsEccentricityType, str]] = ..., eccentricity_ez: _Optional[float] = ..., restraint_spring_about_x: _Optional[float] = ..., restraint_spring_about_z: _Optional[float] = ..., restraint_spring_warping: _Optional[float] = ..., support_in_y_type: _Optional[_Union[AluminumEffectiveLengthsNodalSupportsSupportInYType, str]] = ..., restraint_about_x_type: _Optional[_Union[AluminumEffectiveLengthsNodalSupportsRestraintAboutXType, str]] = ..., restraint_about_z_type: _Optional[_Union[AluminumEffectiveLengthsNodalSupportsRestraintAboutZType, str]] = ..., restraint_warping_type: _Optional[_Union[AluminumEffectiveLengthsNodalSupportsRestraintWarpingType, str]] = ..., nodes: _Optional[_Iterable[int]] = ...) -> None: ...

class AluminumEffectiveLengthsFactorsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[AluminumEffectiveLengthsFactorsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[AluminumEffectiveLengthsFactorsRow, _Mapping]]] = ...) -> None: ...

class AluminumEffectiveLengthsFactorsRow(_message.Message):
    __slots__ = ("no", "description", "flexural_buckling_u", "flexural_buckling_v", "flexural_buckling_y", "flexural_buckling_z", "torsional_buckling", "lateral_torsional_buckling", "lateral_torsional_buckling_top", "lateral_torsional_buckling_bottom", "critical_moment")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_U_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_V_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_Y_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_Z_FIELD_NUMBER: _ClassVar[int]
    TORSIONAL_BUCKLING_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_TOP_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_MOMENT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    flexural_buckling_u: float
    flexural_buckling_v: float
    flexural_buckling_y: float
    flexural_buckling_z: float
    torsional_buckling: float
    lateral_torsional_buckling: float
    lateral_torsional_buckling_top: float
    lateral_torsional_buckling_bottom: float
    critical_moment: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., flexural_buckling_u: _Optional[float] = ..., flexural_buckling_v: _Optional[float] = ..., flexural_buckling_y: _Optional[float] = ..., flexural_buckling_z: _Optional[float] = ..., torsional_buckling: _Optional[float] = ..., lateral_torsional_buckling: _Optional[float] = ..., lateral_torsional_buckling_top: _Optional[float] = ..., lateral_torsional_buckling_bottom: _Optional[float] = ..., critical_moment: _Optional[float] = ...) -> None: ...

class AluminumEffectiveLengthsLengthsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[AluminumEffectiveLengthsLengthsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[AluminumEffectiveLengthsLengthsRow, _Mapping]]] = ...) -> None: ...

class AluminumEffectiveLengthsLengthsRow(_message.Message):
    __slots__ = ("no", "description", "flexural_buckling_u", "flexural_buckling_v", "flexural_buckling_y", "flexural_buckling_z", "torsional_buckling", "lateral_torsional_buckling", "lateral_torsional_buckling_top", "lateral_torsional_buckling_bottom", "critical_moment")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_U_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_V_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_Y_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_Z_FIELD_NUMBER: _ClassVar[int]
    TORSIONAL_BUCKLING_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_TOP_FIELD_NUMBER: _ClassVar[int]
    LATERAL_TORSIONAL_BUCKLING_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_MOMENT_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    flexural_buckling_u: float
    flexural_buckling_v: float
    flexural_buckling_y: float
    flexural_buckling_z: float
    torsional_buckling: float
    lateral_torsional_buckling: float
    lateral_torsional_buckling_top: float
    lateral_torsional_buckling_bottom: float
    critical_moment: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., flexural_buckling_u: _Optional[float] = ..., flexural_buckling_v: _Optional[float] = ..., flexural_buckling_y: _Optional[float] = ..., flexural_buckling_z: _Optional[float] = ..., torsional_buckling: _Optional[float] = ..., lateral_torsional_buckling: _Optional[float] = ..., lateral_torsional_buckling_top: _Optional[float] = ..., lateral_torsional_buckling_bottom: _Optional[float] = ..., critical_moment: _Optional[float] = ...) -> None: ...

class AluminumEffectiveLengthsStabilityImportDataFactorsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[AluminumEffectiveLengthsStabilityImportDataFactorsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[AluminumEffectiveLengthsStabilityImportDataFactorsRow, _Mapping]]] = ...) -> None: ...

class AluminumEffectiveLengthsStabilityImportDataFactorsRow(_message.Message):
    __slots__ = ("no", "description", "flexural_buckling_u", "flexural_buckling_v", "flexural_buckling_y", "flexural_buckling_z")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_U_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_V_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_Y_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_Z_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    flexural_buckling_u: float
    flexural_buckling_v: float
    flexural_buckling_y: float
    flexural_buckling_z: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., flexural_buckling_u: _Optional[float] = ..., flexural_buckling_v: _Optional[float] = ..., flexural_buckling_y: _Optional[float] = ..., flexural_buckling_z: _Optional[float] = ...) -> None: ...

class AluminumEffectiveLengthsStabilityImportDataLengthsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[AluminumEffectiveLengthsStabilityImportDataLengthsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[AluminumEffectiveLengthsStabilityImportDataLengthsRow, _Mapping]]] = ...) -> None: ...

class AluminumEffectiveLengthsStabilityImportDataLengthsRow(_message.Message):
    __slots__ = ("no", "description", "flexural_buckling_u", "flexural_buckling_v", "flexural_buckling_y", "flexural_buckling_z")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_U_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_V_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_Y_FIELD_NUMBER: _ClassVar[int]
    FLEXURAL_BUCKLING_Z_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    flexural_buckling_u: float
    flexural_buckling_v: float
    flexural_buckling_y: float
    flexural_buckling_z: float
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., flexural_buckling_u: _Optional[float] = ..., flexural_buckling_v: _Optional[float] = ..., flexural_buckling_y: _Optional[float] = ..., flexural_buckling_z: _Optional[float] = ...) -> None: ...
