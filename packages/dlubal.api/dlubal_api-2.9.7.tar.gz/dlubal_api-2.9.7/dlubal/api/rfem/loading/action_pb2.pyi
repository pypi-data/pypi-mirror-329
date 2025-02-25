from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActionActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTION_ACTION_TYPE_SIMULTANEOUSLY: _ClassVar[ActionActionType]
    ACTION_ACTION_TYPE_ALTERNATIVELY: _ClassVar[ActionActionType]
    ACTION_ACTION_TYPE_DIFFERENTLY: _ClassVar[ActionActionType]
    ACTION_ACTION_TYPE_DYNAMIC_LOAD_CASE: _ClassVar[ActionActionType]

class ActionImposedLoadCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTION_IMPOSED_LOAD_CATEGORY_UNKNOWN: _ClassVar[ActionImposedLoadCategory]
    ACTION_IMPOSED_LOAD_CATEGORY_IMPOSED_LOADS_CATEGORY_A: _ClassVar[ActionImposedLoadCategory]
    ACTION_IMPOSED_LOAD_CATEGORY_IMPOSED_LOADS_CATEGORY_B: _ClassVar[ActionImposedLoadCategory]
    ACTION_IMPOSED_LOAD_CATEGORY_IMPOSED_LOADS_CATEGORY_C: _ClassVar[ActionImposedLoadCategory]
    ACTION_IMPOSED_LOAD_CATEGORY_IMPOSED_LOADS_CATEGORY_D: _ClassVar[ActionImposedLoadCategory]
    ACTION_IMPOSED_LOAD_CATEGORY_IMPOSED_LOADS_CATEGORY_E: _ClassVar[ActionImposedLoadCategory]
ACTION_ACTION_TYPE_SIMULTANEOUSLY: ActionActionType
ACTION_ACTION_TYPE_ALTERNATIVELY: ActionActionType
ACTION_ACTION_TYPE_DIFFERENTLY: ActionActionType
ACTION_ACTION_TYPE_DYNAMIC_LOAD_CASE: ActionActionType
ACTION_IMPOSED_LOAD_CATEGORY_UNKNOWN: ActionImposedLoadCategory
ACTION_IMPOSED_LOAD_CATEGORY_IMPOSED_LOADS_CATEGORY_A: ActionImposedLoadCategory
ACTION_IMPOSED_LOAD_CATEGORY_IMPOSED_LOADS_CATEGORY_B: ActionImposedLoadCategory
ACTION_IMPOSED_LOAD_CATEGORY_IMPOSED_LOADS_CATEGORY_C: ActionImposedLoadCategory
ACTION_IMPOSED_LOAD_CATEGORY_IMPOSED_LOADS_CATEGORY_D: ActionImposedLoadCategory
ACTION_IMPOSED_LOAD_CATEGORY_IMPOSED_LOADS_CATEGORY_E: ActionImposedLoadCategory

class Action(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "is_active", "action_category", "action_type", "comment", "is_generated", "generating_object_info", "items", "has_short_duration", "has_duration_shorter_than_one_month", "imposed_load_category", "has_short_duration_according_to_5132", "for_temperature_apply_coefficients", "short_time_variable_action", "crane_operated_ware_housing_system_reduced_partial_factor", "has_inclusive_action", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    ACTION_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    HAS_SHORT_DURATION_FIELD_NUMBER: _ClassVar[int]
    HAS_DURATION_SHORTER_THAN_ONE_MONTH_FIELD_NUMBER: _ClassVar[int]
    IMPOSED_LOAD_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    HAS_SHORT_DURATION_ACCORDING_TO_5132_FIELD_NUMBER: _ClassVar[int]
    FOR_TEMPERATURE_APPLY_COEFFICIENTS_FIELD_NUMBER: _ClassVar[int]
    SHORT_TIME_VARIABLE_ACTION_FIELD_NUMBER: _ClassVar[int]
    CRANE_OPERATED_WARE_HOUSING_SYSTEM_REDUCED_PARTIAL_FACTOR_FIELD_NUMBER: _ClassVar[int]
    HAS_INCLUSIVE_ACTION_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    is_active: bool
    action_category: str
    action_type: ActionActionType
    comment: str
    is_generated: bool
    generating_object_info: str
    items: ActionItemsTable
    has_short_duration: bool
    has_duration_shorter_than_one_month: bool
    imposed_load_category: ActionImposedLoadCategory
    has_short_duration_according_to_5132: bool
    for_temperature_apply_coefficients: bool
    short_time_variable_action: bool
    crane_operated_ware_housing_system_reduced_partial_factor: bool
    has_inclusive_action: bool
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., is_active: bool = ..., action_category: _Optional[str] = ..., action_type: _Optional[_Union[ActionActionType, str]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., items: _Optional[_Union[ActionItemsTable, _Mapping]] = ..., has_short_duration: bool = ..., has_duration_shorter_than_one_month: bool = ..., imposed_load_category: _Optional[_Union[ActionImposedLoadCategory, str]] = ..., has_short_duration_according_to_5132: bool = ..., for_temperature_apply_coefficients: bool = ..., short_time_variable_action: bool = ..., crane_operated_ware_housing_system_reduced_partial_factor: bool = ..., has_inclusive_action: bool = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...

class ActionItemsTable(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[ActionItemsRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[ActionItemsRow, _Mapping]]] = ...) -> None: ...

class ActionItemsRow(_message.Message):
    __slots__ = ("no", "description", "load_case_item", "acting_group_number")
    NO_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_ITEM_FIELD_NUMBER: _ClassVar[int]
    ACTING_GROUP_NUMBER_FIELD_NUMBER: _ClassVar[int]
    no: int
    description: str
    load_case_item: int
    acting_group_number: int
    def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., load_case_item: _Optional[int] = ..., acting_group_number: _Optional[int] = ...) -> None: ...
