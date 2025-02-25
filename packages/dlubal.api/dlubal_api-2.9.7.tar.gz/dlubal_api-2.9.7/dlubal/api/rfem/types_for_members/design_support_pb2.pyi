from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DesignSupportType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DESIGN_SUPPORT_TYPE_UNKNOWN: _ClassVar[DesignSupportType]
    DESIGN_SUPPORT_TYPE_DESIGN_SUPPORT_TYPE_CONCRETE: _ClassVar[DesignSupportType]
    DESIGN_SUPPORT_TYPE_DESIGN_SUPPORT_TYPE_GENERAL: _ClassVar[DesignSupportType]
    DESIGN_SUPPORT_TYPE_DESIGN_SUPPORT_TYPE_STEEL: _ClassVar[DesignSupportType]
    DESIGN_SUPPORT_TYPE_DESIGN_SUPPORT_TYPE_TIMBER: _ClassVar[DesignSupportType]

class DesignSupportDesignSupportOrientationY(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DESIGN_SUPPORT_DESIGN_SUPPORT_ORIENTATION_Y_POSITIVE: _ClassVar[DesignSupportDesignSupportOrientationY]
    DESIGN_SUPPORT_DESIGN_SUPPORT_ORIENTATION_Y_BOTH: _ClassVar[DesignSupportDesignSupportOrientationY]
    DESIGN_SUPPORT_DESIGN_SUPPORT_ORIENTATION_Y_NEGATIVE: _ClassVar[DesignSupportDesignSupportOrientationY]

class DesignSupportDesignSupportOrientationZ(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DESIGN_SUPPORT_DESIGN_SUPPORT_ORIENTATION_Z_POSITIVE: _ClassVar[DesignSupportDesignSupportOrientationZ]
    DESIGN_SUPPORT_DESIGN_SUPPORT_ORIENTATION_Z_BOTH: _ClassVar[DesignSupportDesignSupportOrientationZ]
    DESIGN_SUPPORT_DESIGN_SUPPORT_ORIENTATION_Z_NEGATIVE: _ClassVar[DesignSupportDesignSupportOrientationZ]

class DesignSupportTimberCalculationMethodY(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DESIGN_SUPPORT_TIMBER_CALCULATION_METHOD_Y_ACC_TO_4_2_2_2: _ClassVar[DesignSupportTimberCalculationMethodY]
    DESIGN_SUPPORT_TIMBER_CALCULATION_METHOD_Y_ACC_TO_ANNEX_C: _ClassVar[DesignSupportTimberCalculationMethodY]

class DesignSupportTimberCalculationMethodZ(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DESIGN_SUPPORT_TIMBER_CALCULATION_METHOD_Z_ACC_TO_4_2_2_2: _ClassVar[DesignSupportTimberCalculationMethodZ]
    DESIGN_SUPPORT_TIMBER_CALCULATION_METHOD_Z_ACC_TO_ANNEX_C: _ClassVar[DesignSupportTimberCalculationMethodZ]

class DesignSupportTimberCompressionDesignValueY(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DESIGN_SUPPORT_TIMBER_COMPRESSION_DESIGN_VALUE_Y_0_0_4: _ClassVar[DesignSupportTimberCompressionDesignValueY]
    DESIGN_SUPPORT_TIMBER_COMPRESSION_DESIGN_VALUE_Y_0_0_2: _ClassVar[DesignSupportTimberCompressionDesignValueY]

class DesignSupportTimberCompressionDesignValueZ(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DESIGN_SUPPORT_TIMBER_COMPRESSION_DESIGN_VALUE_Z_0_0_4: _ClassVar[DesignSupportTimberCompressionDesignValueZ]
    DESIGN_SUPPORT_TIMBER_COMPRESSION_DESIGN_VALUE_Z_0_0_2: _ClassVar[DesignSupportTimberCompressionDesignValueZ]
DESIGN_SUPPORT_TYPE_UNKNOWN: DesignSupportType
DESIGN_SUPPORT_TYPE_DESIGN_SUPPORT_TYPE_CONCRETE: DesignSupportType
DESIGN_SUPPORT_TYPE_DESIGN_SUPPORT_TYPE_GENERAL: DesignSupportType
DESIGN_SUPPORT_TYPE_DESIGN_SUPPORT_TYPE_STEEL: DesignSupportType
DESIGN_SUPPORT_TYPE_DESIGN_SUPPORT_TYPE_TIMBER: DesignSupportType
DESIGN_SUPPORT_DESIGN_SUPPORT_ORIENTATION_Y_POSITIVE: DesignSupportDesignSupportOrientationY
DESIGN_SUPPORT_DESIGN_SUPPORT_ORIENTATION_Y_BOTH: DesignSupportDesignSupportOrientationY
DESIGN_SUPPORT_DESIGN_SUPPORT_ORIENTATION_Y_NEGATIVE: DesignSupportDesignSupportOrientationY
DESIGN_SUPPORT_DESIGN_SUPPORT_ORIENTATION_Z_POSITIVE: DesignSupportDesignSupportOrientationZ
DESIGN_SUPPORT_DESIGN_SUPPORT_ORIENTATION_Z_BOTH: DesignSupportDesignSupportOrientationZ
DESIGN_SUPPORT_DESIGN_SUPPORT_ORIENTATION_Z_NEGATIVE: DesignSupportDesignSupportOrientationZ
DESIGN_SUPPORT_TIMBER_CALCULATION_METHOD_Y_ACC_TO_4_2_2_2: DesignSupportTimberCalculationMethodY
DESIGN_SUPPORT_TIMBER_CALCULATION_METHOD_Y_ACC_TO_ANNEX_C: DesignSupportTimberCalculationMethodY
DESIGN_SUPPORT_TIMBER_CALCULATION_METHOD_Z_ACC_TO_4_2_2_2: DesignSupportTimberCalculationMethodZ
DESIGN_SUPPORT_TIMBER_CALCULATION_METHOD_Z_ACC_TO_ANNEX_C: DesignSupportTimberCalculationMethodZ
DESIGN_SUPPORT_TIMBER_COMPRESSION_DESIGN_VALUE_Y_0_0_4: DesignSupportTimberCompressionDesignValueY
DESIGN_SUPPORT_TIMBER_COMPRESSION_DESIGN_VALUE_Y_0_0_2: DesignSupportTimberCompressionDesignValueY
DESIGN_SUPPORT_TIMBER_COMPRESSION_DESIGN_VALUE_Z_0_0_4: DesignSupportTimberCompressionDesignValueZ
DESIGN_SUPPORT_TIMBER_COMPRESSION_DESIGN_VALUE_Z_0_0_2: DesignSupportTimberCompressionDesignValueZ

class DesignSupport(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "assigned_to_members", "assigned_to_member_sets", "assigned_to_nodes", "assigned_to_objects", "comment", "is_generated", "generating_object_info", "activate_in_y", "activate_in_z", "consider_in_deflection_design_y", "consider_in_deflection_design_z", "concrete_monolithic_connection_z_enabled", "concrete_ratio_of_moment_redistribution_z", "design_support_orientation_y", "design_support_orientation_z", "direct_support_y_enabled", "direct_support_z_enabled", "inner_support_y_enabled", "inner_support_z_enabled", "limit_of_high_bending_stresses_y", "limit_of_high_bending_stresses_z", "consider_in_fire_design_y", "consider_in_fire_design_z", "support_depth_by_section_width_of_member_y_enabled", "support_depth_by_section_width_of_member_z_enabled", "support_depth_y", "support_depth_z", "support_width_y", "support_width_z", "timber_allow_higher_deformation_y_enabled", "timber_allow_higher_deformation_z_enabled", "timber_calculation_method_y", "timber_calculation_method_z", "timber_check_critical_bearing_y_enabled", "timber_check_critical_bearing_z_enabled", "timber_compression_design_value_y", "timber_compression_design_value_z", "timber_factor_of_compression_y", "timber_factor_of_compression_z", "end_support_z_enabled", "overhang_length_z", "fastened_to_support_z_enabled", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_NODES_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_IN_Y_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_IN_Z_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_IN_DEFLECTION_DESIGN_Y_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_IN_DEFLECTION_DESIGN_Z_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_MONOLITHIC_CONNECTION_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_RATIO_OF_MOMENT_REDISTRIBUTION_Z_FIELD_NUMBER: _ClassVar[int]
    DESIGN_SUPPORT_ORIENTATION_Y_FIELD_NUMBER: _ClassVar[int]
    DESIGN_SUPPORT_ORIENTATION_Z_FIELD_NUMBER: _ClassVar[int]
    DIRECT_SUPPORT_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DIRECT_SUPPORT_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    INNER_SUPPORT_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    INNER_SUPPORT_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    LIMIT_OF_HIGH_BENDING_STRESSES_Y_FIELD_NUMBER: _ClassVar[int]
    LIMIT_OF_HIGH_BENDING_STRESSES_Z_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_IN_FIRE_DESIGN_Y_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_IN_FIRE_DESIGN_Z_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_DEPTH_BY_SECTION_WIDTH_OF_MEMBER_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_DEPTH_BY_SECTION_WIDTH_OF_MEMBER_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_DEPTH_Y_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_DEPTH_Z_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_WIDTH_Y_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_WIDTH_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_ALLOW_HIGHER_DEFORMATION_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TIMBER_ALLOW_HIGHER_DEFORMATION_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TIMBER_CALCULATION_METHOD_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_CALCULATION_METHOD_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_CHECK_CRITICAL_BEARING_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TIMBER_CHECK_CRITICAL_BEARING_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TIMBER_COMPRESSION_DESIGN_VALUE_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_COMPRESSION_DESIGN_VALUE_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_FACTOR_OF_COMPRESSION_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_FACTOR_OF_COMPRESSION_Z_FIELD_NUMBER: _ClassVar[int]
    END_SUPPORT_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    OVERHANG_LENGTH_Z_FIELD_NUMBER: _ClassVar[int]
    FASTENED_TO_SUPPORT_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: DesignSupportType
    user_defined_name_enabled: bool
    name: str
    assigned_to_members: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_member_sets: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_nodes: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_objects: str
    comment: str
    is_generated: bool
    generating_object_info: str
    activate_in_y: bool
    activate_in_z: bool
    consider_in_deflection_design_y: bool
    consider_in_deflection_design_z: bool
    concrete_monolithic_connection_z_enabled: bool
    concrete_ratio_of_moment_redistribution_z: float
    design_support_orientation_y: DesignSupportDesignSupportOrientationY
    design_support_orientation_z: DesignSupportDesignSupportOrientationZ
    direct_support_y_enabled: bool
    direct_support_z_enabled: bool
    inner_support_y_enabled: bool
    inner_support_z_enabled: bool
    limit_of_high_bending_stresses_y: float
    limit_of_high_bending_stresses_z: float
    consider_in_fire_design_y: bool
    consider_in_fire_design_z: bool
    support_depth_by_section_width_of_member_y_enabled: bool
    support_depth_by_section_width_of_member_z_enabled: bool
    support_depth_y: float
    support_depth_z: float
    support_width_y: float
    support_width_z: float
    timber_allow_higher_deformation_y_enabled: bool
    timber_allow_higher_deformation_z_enabled: bool
    timber_calculation_method_y: DesignSupportTimberCalculationMethodY
    timber_calculation_method_z: DesignSupportTimberCalculationMethodZ
    timber_check_critical_bearing_y_enabled: bool
    timber_check_critical_bearing_z_enabled: bool
    timber_compression_design_value_y: DesignSupportTimberCompressionDesignValueY
    timber_compression_design_value_z: DesignSupportTimberCompressionDesignValueZ
    timber_factor_of_compression_y: float
    timber_factor_of_compression_z: float
    end_support_z_enabled: bool
    overhang_length_z: float
    fastened_to_support_z_enabled: bool
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[DesignSupportType, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to_members: _Optional[_Iterable[int]] = ..., assigned_to_member_sets: _Optional[_Iterable[int]] = ..., assigned_to_nodes: _Optional[_Iterable[int]] = ..., assigned_to_objects: _Optional[str] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., activate_in_y: bool = ..., activate_in_z: bool = ..., consider_in_deflection_design_y: bool = ..., consider_in_deflection_design_z: bool = ..., concrete_monolithic_connection_z_enabled: bool = ..., concrete_ratio_of_moment_redistribution_z: _Optional[float] = ..., design_support_orientation_y: _Optional[_Union[DesignSupportDesignSupportOrientationY, str]] = ..., design_support_orientation_z: _Optional[_Union[DesignSupportDesignSupportOrientationZ, str]] = ..., direct_support_y_enabled: bool = ..., direct_support_z_enabled: bool = ..., inner_support_y_enabled: bool = ..., inner_support_z_enabled: bool = ..., limit_of_high_bending_stresses_y: _Optional[float] = ..., limit_of_high_bending_stresses_z: _Optional[float] = ..., consider_in_fire_design_y: bool = ..., consider_in_fire_design_z: bool = ..., support_depth_by_section_width_of_member_y_enabled: bool = ..., support_depth_by_section_width_of_member_z_enabled: bool = ..., support_depth_y: _Optional[float] = ..., support_depth_z: _Optional[float] = ..., support_width_y: _Optional[float] = ..., support_width_z: _Optional[float] = ..., timber_allow_higher_deformation_y_enabled: bool = ..., timber_allow_higher_deformation_z_enabled: bool = ..., timber_calculation_method_y: _Optional[_Union[DesignSupportTimberCalculationMethodY, str]] = ..., timber_calculation_method_z: _Optional[_Union[DesignSupportTimberCalculationMethodZ, str]] = ..., timber_check_critical_bearing_y_enabled: bool = ..., timber_check_critical_bearing_z_enabled: bool = ..., timber_compression_design_value_y: _Optional[_Union[DesignSupportTimberCompressionDesignValueY, str]] = ..., timber_compression_design_value_z: _Optional[_Union[DesignSupportTimberCompressionDesignValueZ, str]] = ..., timber_factor_of_compression_y: _Optional[float] = ..., timber_factor_of_compression_z: _Optional[float] = ..., end_support_z_enabled: bool = ..., overhang_length_z: _Optional[float] = ..., fastened_to_support_z_enabled: bool = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
