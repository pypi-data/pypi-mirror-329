from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpectralAnalysisSettingsCombinationRuleForPeriodicResponses(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_PERIODIC_RESPONSES_SRSS: _ClassVar[SpectralAnalysisSettingsCombinationRuleForPeriodicResponses]
    SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_PERIODIC_RESPONSES_ABSOLUTE_SUM: _ClassVar[SpectralAnalysisSettingsCombinationRuleForPeriodicResponses]
    SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_PERIODIC_RESPONSES_CQC: _ClassVar[SpectralAnalysisSettingsCombinationRuleForPeriodicResponses]

class SpectralAnalysisSettingsCombinationRuleForMissingMasses(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_MISSING_MASSES_SRSS: _ClassVar[SpectralAnalysisSettingsCombinationRuleForMissingMasses]
    SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_MISSING_MASSES_ABSOLUTE_SUM: _ClassVar[SpectralAnalysisSettingsCombinationRuleForMissingMasses]

class SpectralAnalysisSettingsCombinationRuleForDirectionalComponents(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_DIRECTIONAL_COMPONENTS_SRSS: _ClassVar[SpectralAnalysisSettingsCombinationRuleForDirectionalComponents]
    SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_DIRECTIONAL_COMPONENTS_ABSOLUTE_SUM: _ClassVar[SpectralAnalysisSettingsCombinationRuleForDirectionalComponents]
    SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_DIRECTIONAL_COMPONENTS_SCALED_SUM: _ClassVar[SpectralAnalysisSettingsCombinationRuleForDirectionalComponents]

class SpectralAnalysisSettingsDampingForCqcRule(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPECTRAL_ANALYSIS_SETTINGS_DAMPING_FOR_CQC_RULE_CONSTANT_FOR_EACH_MODE: _ClassVar[SpectralAnalysisSettingsDampingForCqcRule]
    SPECTRAL_ANALYSIS_SETTINGS_DAMPING_FOR_CQC_RULE_DIFFERENT_FOR_EACH_MODE: _ClassVar[SpectralAnalysisSettingsDampingForCqcRule]

class SpectralAnalysisSettingsZeroPeriodicAccelerationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPECTRAL_ANALYSIS_SETTINGS_ZERO_PERIODIC_ACCELERATION_TYPE_ACCORDING_TO_RESPONSE_SPECTRUM: _ClassVar[SpectralAnalysisSettingsZeroPeriodicAccelerationType]
    SPECTRAL_ANALYSIS_SETTINGS_ZERO_PERIODIC_ACCELERATION_TYPE_SPECTRAL_ACCELERATION_OF_LAST_CALCULATED_FREQUENCY: _ClassVar[SpectralAnalysisSettingsZeroPeriodicAccelerationType]
    SPECTRAL_ANALYSIS_SETTINGS_ZERO_PERIODIC_ACCELERATION_TYPE_USER_DEFINED: _ClassVar[SpectralAnalysisSettingsZeroPeriodicAccelerationType]
SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_PERIODIC_RESPONSES_SRSS: SpectralAnalysisSettingsCombinationRuleForPeriodicResponses
SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_PERIODIC_RESPONSES_ABSOLUTE_SUM: SpectralAnalysisSettingsCombinationRuleForPeriodicResponses
SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_PERIODIC_RESPONSES_CQC: SpectralAnalysisSettingsCombinationRuleForPeriodicResponses
SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_MISSING_MASSES_SRSS: SpectralAnalysisSettingsCombinationRuleForMissingMasses
SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_MISSING_MASSES_ABSOLUTE_SUM: SpectralAnalysisSettingsCombinationRuleForMissingMasses
SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_DIRECTIONAL_COMPONENTS_SRSS: SpectralAnalysisSettingsCombinationRuleForDirectionalComponents
SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_DIRECTIONAL_COMPONENTS_ABSOLUTE_SUM: SpectralAnalysisSettingsCombinationRuleForDirectionalComponents
SPECTRAL_ANALYSIS_SETTINGS_COMBINATION_RULE_FOR_DIRECTIONAL_COMPONENTS_SCALED_SUM: SpectralAnalysisSettingsCombinationRuleForDirectionalComponents
SPECTRAL_ANALYSIS_SETTINGS_DAMPING_FOR_CQC_RULE_CONSTANT_FOR_EACH_MODE: SpectralAnalysisSettingsDampingForCqcRule
SPECTRAL_ANALYSIS_SETTINGS_DAMPING_FOR_CQC_RULE_DIFFERENT_FOR_EACH_MODE: SpectralAnalysisSettingsDampingForCqcRule
SPECTRAL_ANALYSIS_SETTINGS_ZERO_PERIODIC_ACCELERATION_TYPE_ACCORDING_TO_RESPONSE_SPECTRUM: SpectralAnalysisSettingsZeroPeriodicAccelerationType
SPECTRAL_ANALYSIS_SETTINGS_ZERO_PERIODIC_ACCELERATION_TYPE_SPECTRAL_ACCELERATION_OF_LAST_CALCULATED_FREQUENCY: SpectralAnalysisSettingsZeroPeriodicAccelerationType
SPECTRAL_ANALYSIS_SETTINGS_ZERO_PERIODIC_ACCELERATION_TYPE_USER_DEFINED: SpectralAnalysisSettingsZeroPeriodicAccelerationType

class SpectralAnalysisSettings(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "comment", "assigned_to", "combination_rule_for_periodic_responses", "use_equivalent_linear_combination", "include_missing_masses", "combination_rule_for_missing_masses", "save_results_of_all_selected_modes", "combination_rule_for_directional_components", "combination_rule_for_directional_components_value", "damping_for_cqc_rule", "constant_d_for_each_mode", "zero_periodic_acceleration_type", "user_defined_zpa", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_FIELD_NUMBER: _ClassVar[int]
    COMBINATION_RULE_FOR_PERIODIC_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    USE_EQUIVALENT_LINEAR_COMBINATION_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_MISSING_MASSES_FIELD_NUMBER: _ClassVar[int]
    COMBINATION_RULE_FOR_MISSING_MASSES_FIELD_NUMBER: _ClassVar[int]
    SAVE_RESULTS_OF_ALL_SELECTED_MODES_FIELD_NUMBER: _ClassVar[int]
    COMBINATION_RULE_FOR_DIRECTIONAL_COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    COMBINATION_RULE_FOR_DIRECTIONAL_COMPONENTS_VALUE_FIELD_NUMBER: _ClassVar[int]
    DAMPING_FOR_CQC_RULE_FIELD_NUMBER: _ClassVar[int]
    CONSTANT_D_FOR_EACH_MODE_FIELD_NUMBER: _ClassVar[int]
    ZERO_PERIODIC_ACCELERATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_ZPA_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    comment: str
    assigned_to: str
    combination_rule_for_periodic_responses: SpectralAnalysisSettingsCombinationRuleForPeriodicResponses
    use_equivalent_linear_combination: bool
    include_missing_masses: bool
    combination_rule_for_missing_masses: SpectralAnalysisSettingsCombinationRuleForMissingMasses
    save_results_of_all_selected_modes: bool
    combination_rule_for_directional_components: SpectralAnalysisSettingsCombinationRuleForDirectionalComponents
    combination_rule_for_directional_components_value: float
    damping_for_cqc_rule: SpectralAnalysisSettingsDampingForCqcRule
    constant_d_for_each_mode: float
    zero_periodic_acceleration_type: SpectralAnalysisSettingsZeroPeriodicAccelerationType
    user_defined_zpa: float
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., comment: _Optional[str] = ..., assigned_to: _Optional[str] = ..., combination_rule_for_periodic_responses: _Optional[_Union[SpectralAnalysisSettingsCombinationRuleForPeriodicResponses, str]] = ..., use_equivalent_linear_combination: bool = ..., include_missing_masses: bool = ..., combination_rule_for_missing_masses: _Optional[_Union[SpectralAnalysisSettingsCombinationRuleForMissingMasses, str]] = ..., save_results_of_all_selected_modes: bool = ..., combination_rule_for_directional_components: _Optional[_Union[SpectralAnalysisSettingsCombinationRuleForDirectionalComponents, str]] = ..., combination_rule_for_directional_components_value: _Optional[float] = ..., damping_for_cqc_rule: _Optional[_Union[SpectralAnalysisSettingsDampingForCqcRule, str]] = ..., constant_d_for_each_mode: _Optional[float] = ..., zero_periodic_acceleration_type: _Optional[_Union[SpectralAnalysisSettingsZeroPeriodicAccelerationType, str]] = ..., user_defined_zpa: _Optional[float] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
