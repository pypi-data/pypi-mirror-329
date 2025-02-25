from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TimberServiceConditionsMoistureServiceCondition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_UNKNOWN: _ClassVar[TimberServiceConditionsMoistureServiceCondition]
    TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_DRY: _ClassVar[TimberServiceConditionsMoistureServiceCondition]
    TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_MOIST: _ClassVar[TimberServiceConditionsMoistureServiceCondition]
    TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_RATHER_DRY: _ClassVar[TimberServiceConditionsMoistureServiceCondition]
    TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_RATHER_WET: _ClassVar[TimberServiceConditionsMoistureServiceCondition]
    TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_VERY_DRY: _ClassVar[TimberServiceConditionsMoistureServiceCondition]
    TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_WET: _ClassVar[TimberServiceConditionsMoistureServiceCondition]

class TimberServiceConditionsTreatment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_SERVICE_CONDITIONS_TREATMENT_UNKNOWN: _ClassVar[TimberServiceConditionsTreatment]
    TIMBER_SERVICE_CONDITIONS_TREATMENT_FIRE_RETARDANT: _ClassVar[TimberServiceConditionsTreatment]
    TIMBER_SERVICE_CONDITIONS_TREATMENT_NONE: _ClassVar[TimberServiceConditionsTreatment]
    TIMBER_SERVICE_CONDITIONS_TREATMENT_PRESERVATIVE: _ClassVar[TimberServiceConditionsTreatment]

class TimberServiceConditionsTemperature(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMBER_SERVICE_CONDITIONS_TEMPERATURE_UNKNOWN: _ClassVar[TimberServiceConditionsTemperature]
    TIMBER_SERVICE_CONDITIONS_TEMPERATURE_EQUAL_TO_50: _ClassVar[TimberServiceConditionsTemperature]
    TIMBER_SERVICE_CONDITIONS_TEMPERATURE_LESS_OR_EQUAL_100: _ClassVar[TimberServiceConditionsTemperature]
    TIMBER_SERVICE_CONDITIONS_TEMPERATURE_LESS_OR_EQUAL_35: _ClassVar[TimberServiceConditionsTemperature]
    TIMBER_SERVICE_CONDITIONS_TEMPERATURE_RANGE_100_125: _ClassVar[TimberServiceConditionsTemperature]
    TIMBER_SERVICE_CONDITIONS_TEMPERATURE_RANGE_125_150: _ClassVar[TimberServiceConditionsTemperature]
    TIMBER_SERVICE_CONDITIONS_TEMPERATURE_RANGE_35_50: _ClassVar[TimberServiceConditionsTemperature]
    TIMBER_SERVICE_CONDITIONS_TEMPERATURE_TEMPERATURE_ZONE_1: _ClassVar[TimberServiceConditionsTemperature]
    TIMBER_SERVICE_CONDITIONS_TEMPERATURE_TEMPERATURE_ZONE_2: _ClassVar[TimberServiceConditionsTemperature]
    TIMBER_SERVICE_CONDITIONS_TEMPERATURE_TEMPERATURE_ZONE_3: _ClassVar[TimberServiceConditionsTemperature]
TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_UNKNOWN: TimberServiceConditionsMoistureServiceCondition
TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_DRY: TimberServiceConditionsMoistureServiceCondition
TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_MOIST: TimberServiceConditionsMoistureServiceCondition
TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_RATHER_DRY: TimberServiceConditionsMoistureServiceCondition
TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_RATHER_WET: TimberServiceConditionsMoistureServiceCondition
TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_VERY_DRY: TimberServiceConditionsMoistureServiceCondition
TIMBER_SERVICE_CONDITIONS_MOISTURE_SERVICE_CONDITION_WET: TimberServiceConditionsMoistureServiceCondition
TIMBER_SERVICE_CONDITIONS_TREATMENT_UNKNOWN: TimberServiceConditionsTreatment
TIMBER_SERVICE_CONDITIONS_TREATMENT_FIRE_RETARDANT: TimberServiceConditionsTreatment
TIMBER_SERVICE_CONDITIONS_TREATMENT_NONE: TimberServiceConditionsTreatment
TIMBER_SERVICE_CONDITIONS_TREATMENT_PRESERVATIVE: TimberServiceConditionsTreatment
TIMBER_SERVICE_CONDITIONS_TEMPERATURE_UNKNOWN: TimberServiceConditionsTemperature
TIMBER_SERVICE_CONDITIONS_TEMPERATURE_EQUAL_TO_50: TimberServiceConditionsTemperature
TIMBER_SERVICE_CONDITIONS_TEMPERATURE_LESS_OR_EQUAL_100: TimberServiceConditionsTemperature
TIMBER_SERVICE_CONDITIONS_TEMPERATURE_LESS_OR_EQUAL_35: TimberServiceConditionsTemperature
TIMBER_SERVICE_CONDITIONS_TEMPERATURE_RANGE_100_125: TimberServiceConditionsTemperature
TIMBER_SERVICE_CONDITIONS_TEMPERATURE_RANGE_125_150: TimberServiceConditionsTemperature
TIMBER_SERVICE_CONDITIONS_TEMPERATURE_RANGE_35_50: TimberServiceConditionsTemperature
TIMBER_SERVICE_CONDITIONS_TEMPERATURE_TEMPERATURE_ZONE_1: TimberServiceConditionsTemperature
TIMBER_SERVICE_CONDITIONS_TEMPERATURE_TEMPERATURE_ZONE_2: TimberServiceConditionsTemperature
TIMBER_SERVICE_CONDITIONS_TEMPERATURE_TEMPERATURE_ZONE_3: TimberServiceConditionsTemperature

class TimberServiceConditions(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "members", "member_sets", "surfaces", "surface_sets", "assigned_to_objects", "moisture_service_condition", "treatment", "temperature", "outdoor_environment", "long_term_high_temperature_of_surface", "permanent_load_design_situation", "timber_structures", "short_term_construction_or_maintenance", "timber_is_point_impregnated", "member_pressure_treated", "equilibrium_moisture_content", "user_defined_temperature", "impregnation_with_flame_retardant_under_pressure", "comment", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    SURFACES_FIELD_NUMBER: _ClassVar[int]
    SURFACE_SETS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    MOISTURE_SERVICE_CONDITION_FIELD_NUMBER: _ClassVar[int]
    TREATMENT_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    OUTDOOR_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    LONG_TERM_HIGH_TEMPERATURE_OF_SURFACE_FIELD_NUMBER: _ClassVar[int]
    PERMANENT_LOAD_DESIGN_SITUATION_FIELD_NUMBER: _ClassVar[int]
    TIMBER_STRUCTURES_FIELD_NUMBER: _ClassVar[int]
    SHORT_TERM_CONSTRUCTION_OR_MAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    TIMBER_IS_POINT_IMPREGNATED_FIELD_NUMBER: _ClassVar[int]
    MEMBER_PRESSURE_TREATED_FIELD_NUMBER: _ClassVar[int]
    EQUILIBRIUM_MOISTURE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    IMPREGNATION_WITH_FLAME_RETARDANT_UNDER_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    members: _containers.RepeatedScalarFieldContainer[int]
    member_sets: _containers.RepeatedScalarFieldContainer[int]
    surfaces: _containers.RepeatedScalarFieldContainer[int]
    surface_sets: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_objects: str
    moisture_service_condition: TimberServiceConditionsMoistureServiceCondition
    treatment: TimberServiceConditionsTreatment
    temperature: TimberServiceConditionsTemperature
    outdoor_environment: bool
    long_term_high_temperature_of_surface: bool
    permanent_load_design_situation: bool
    timber_structures: bool
    short_term_construction_or_maintenance: bool
    timber_is_point_impregnated: bool
    member_pressure_treated: bool
    equilibrium_moisture_content: float
    user_defined_temperature: float
    impregnation_with_flame_retardant_under_pressure: bool
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., members: _Optional[_Iterable[int]] = ..., member_sets: _Optional[_Iterable[int]] = ..., surfaces: _Optional[_Iterable[int]] = ..., surface_sets: _Optional[_Iterable[int]] = ..., assigned_to_objects: _Optional[str] = ..., moisture_service_condition: _Optional[_Union[TimberServiceConditionsMoistureServiceCondition, str]] = ..., treatment: _Optional[_Union[TimberServiceConditionsTreatment, str]] = ..., temperature: _Optional[_Union[TimberServiceConditionsTemperature, str]] = ..., outdoor_environment: bool = ..., long_term_high_temperature_of_surface: bool = ..., permanent_load_design_situation: bool = ..., timber_structures: bool = ..., short_term_construction_or_maintenance: bool = ..., timber_is_point_impregnated: bool = ..., member_pressure_treated: bool = ..., equilibrium_moisture_content: _Optional[float] = ..., user_defined_temperature: _Optional[float] = ..., impregnation_with_flame_retardant_under_pressure: bool = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
