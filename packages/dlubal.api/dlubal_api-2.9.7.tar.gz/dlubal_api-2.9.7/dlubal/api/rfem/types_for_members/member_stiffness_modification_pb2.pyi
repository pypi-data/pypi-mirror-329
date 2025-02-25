from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberStiffnessModificationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_STIFFNESS_MODIFICATION_TYPE_UNKNOWN: _ClassVar[MemberStiffnessModificationType]
    MEMBER_STIFFNESS_MODIFICATION_TYPE_ALUMINUM_STRUCTURES_ADM_2020: _ClassVar[MemberStiffnessModificationType]
    MEMBER_STIFFNESS_MODIFICATION_TYPE_CONCRETE_STRUCTURES_ACI: _ClassVar[MemberStiffnessModificationType]
    MEMBER_STIFFNESS_MODIFICATION_TYPE_CONCRETE_STRUCTURES_CSA: _ClassVar[MemberStiffnessModificationType]
    MEMBER_STIFFNESS_MODIFICATION_TYPE_PARTIAL_STIFFNESSES_FACTORS: _ClassVar[MemberStiffnessModificationType]
    MEMBER_STIFFNESS_MODIFICATION_TYPE_STEEL_STRUCTURES_360_10: _ClassVar[MemberStiffnessModificationType]
    MEMBER_STIFFNESS_MODIFICATION_TYPE_STEEL_STRUCTURES_360_16: _ClassVar[MemberStiffnessModificationType]
    MEMBER_STIFFNESS_MODIFICATION_TYPE_STEEL_STRUCTURES_360_22: _ClassVar[MemberStiffnessModificationType]
    MEMBER_STIFFNESS_MODIFICATION_TYPE_STEEL_STRUCTURES_CSA_S136_16: _ClassVar[MemberStiffnessModificationType]
    MEMBER_STIFFNESS_MODIFICATION_TYPE_STEEL_STRUCTURES_CSA_S16_19: _ClassVar[MemberStiffnessModificationType]
    MEMBER_STIFFNESS_MODIFICATION_TYPE_STEEL_STRUCTURES_S100_16: _ClassVar[MemberStiffnessModificationType]
    MEMBER_STIFFNESS_MODIFICATION_TYPE_TOTAL_STIFFNESSES_FACTORS: _ClassVar[MemberStiffnessModificationType]

class MemberStiffnessModificationSteelStructureCsaDetermineTauB(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_STIFFNESS_MODIFICATION_STEEL_STRUCTURE_CSA_DETERMINE_TAU_B_ITERATIVE: _ClassVar[MemberStiffnessModificationSteelStructureCsaDetermineTauB]
    MEMBER_STIFFNESS_MODIFICATION_STEEL_STRUCTURE_CSA_DETERMINE_TAU_B_SET_TO_1: _ClassVar[MemberStiffnessModificationSteelStructureCsaDetermineTauB]

class MemberStiffnessModificationSteelStructureDetermineTauB(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_STIFFNESS_MODIFICATION_STEEL_STRUCTURE_DETERMINE_TAU_B_ITERATIVE: _ClassVar[MemberStiffnessModificationSteelStructureDetermineTauB]
    MEMBER_STIFFNESS_MODIFICATION_STEEL_STRUCTURE_DETERMINE_TAU_B_SET_TO_1: _ClassVar[MemberStiffnessModificationSteelStructureDetermineTauB]

class MemberStiffnessModificationSteelStructureDesignMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_STIFFNESS_MODIFICATION_STEEL_STRUCTURE_DESIGN_METHOD_LRFD: _ClassVar[MemberStiffnessModificationSteelStructureDesignMethod]
    MEMBER_STIFFNESS_MODIFICATION_STEEL_STRUCTURE_DESIGN_METHOD_ASD: _ClassVar[MemberStiffnessModificationSteelStructureDesignMethod]

class MemberStiffnessModificationConcreteStructureComponentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_STIFFNESS_MODIFICATION_CONCRETE_STRUCTURE_COMPONENT_TYPE_COLUMNS: _ClassVar[MemberStiffnessModificationConcreteStructureComponentType]
    MEMBER_STIFFNESS_MODIFICATION_CONCRETE_STRUCTURE_COMPONENT_TYPE_BEAMS: _ClassVar[MemberStiffnessModificationConcreteStructureComponentType]
MEMBER_STIFFNESS_MODIFICATION_TYPE_UNKNOWN: MemberStiffnessModificationType
MEMBER_STIFFNESS_MODIFICATION_TYPE_ALUMINUM_STRUCTURES_ADM_2020: MemberStiffnessModificationType
MEMBER_STIFFNESS_MODIFICATION_TYPE_CONCRETE_STRUCTURES_ACI: MemberStiffnessModificationType
MEMBER_STIFFNESS_MODIFICATION_TYPE_CONCRETE_STRUCTURES_CSA: MemberStiffnessModificationType
MEMBER_STIFFNESS_MODIFICATION_TYPE_PARTIAL_STIFFNESSES_FACTORS: MemberStiffnessModificationType
MEMBER_STIFFNESS_MODIFICATION_TYPE_STEEL_STRUCTURES_360_10: MemberStiffnessModificationType
MEMBER_STIFFNESS_MODIFICATION_TYPE_STEEL_STRUCTURES_360_16: MemberStiffnessModificationType
MEMBER_STIFFNESS_MODIFICATION_TYPE_STEEL_STRUCTURES_360_22: MemberStiffnessModificationType
MEMBER_STIFFNESS_MODIFICATION_TYPE_STEEL_STRUCTURES_CSA_S136_16: MemberStiffnessModificationType
MEMBER_STIFFNESS_MODIFICATION_TYPE_STEEL_STRUCTURES_CSA_S16_19: MemberStiffnessModificationType
MEMBER_STIFFNESS_MODIFICATION_TYPE_STEEL_STRUCTURES_S100_16: MemberStiffnessModificationType
MEMBER_STIFFNESS_MODIFICATION_TYPE_TOTAL_STIFFNESSES_FACTORS: MemberStiffnessModificationType
MEMBER_STIFFNESS_MODIFICATION_STEEL_STRUCTURE_CSA_DETERMINE_TAU_B_ITERATIVE: MemberStiffnessModificationSteelStructureCsaDetermineTauB
MEMBER_STIFFNESS_MODIFICATION_STEEL_STRUCTURE_CSA_DETERMINE_TAU_B_SET_TO_1: MemberStiffnessModificationSteelStructureCsaDetermineTauB
MEMBER_STIFFNESS_MODIFICATION_STEEL_STRUCTURE_DETERMINE_TAU_B_ITERATIVE: MemberStiffnessModificationSteelStructureDetermineTauB
MEMBER_STIFFNESS_MODIFICATION_STEEL_STRUCTURE_DETERMINE_TAU_B_SET_TO_1: MemberStiffnessModificationSteelStructureDetermineTauB
MEMBER_STIFFNESS_MODIFICATION_STEEL_STRUCTURE_DESIGN_METHOD_LRFD: MemberStiffnessModificationSteelStructureDesignMethod
MEMBER_STIFFNESS_MODIFICATION_STEEL_STRUCTURE_DESIGN_METHOD_ASD: MemberStiffnessModificationSteelStructureDesignMethod
MEMBER_STIFFNESS_MODIFICATION_CONCRETE_STRUCTURE_COMPONENT_TYPE_COLUMNS: MemberStiffnessModificationConcreteStructureComponentType
MEMBER_STIFFNESS_MODIFICATION_CONCRETE_STRUCTURE_COMPONENT_TYPE_BEAMS: MemberStiffnessModificationConcreteStructureComponentType

class MemberStiffnessModification(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "factor_of_axial_stiffness", "factor_of_bending_y_stiffness", "factor_of_bending_z_stiffness", "partial_stiffness_factor_of_shear_y_stiffness", "partial_stiffness_factor_of_shear_z_stiffness", "partial_stiffness_factor_of_torsion_stiffness", "partial_stiffness_factor_of_weight", "total_stiffness_factor_of_total_stiffness", "steel_structure_csa_stiffness_factor_of_shear_y_stiffness", "steel_structure_csa_stiffness_factor_of_shear_z_stiffness", "steel_structure_csa_stiffness_factor_of_torsion_stiffness", "steel_structure_csa_factor_of_axial_stiffness_enable", "steel_structure_csa_factor_of_bending_y_stiffness_enable", "steel_structure_csa_factor_of_bending_z_stiffness_enable", "steel_structure_csa_factor_of_shear_y_stiffness_enable", "steel_structure_csa_factor_of_shear_z_stiffness_enable", "steel_structure_csa_stiffness_factor_of_torsion_stiffness_enable", "steel_structure_csa_determine_tau_b", "steel_structure_gb_direct_method_enabled", "steel_structure_determine_tau_b", "steel_structure_design_method", "concrete_structure_component_type", "assigned_to_structure_modification", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FACTOR_OF_AXIAL_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
    FACTOR_OF_BENDING_Y_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
    FACTOR_OF_BENDING_Z_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_STIFFNESS_FACTOR_OF_SHEAR_Y_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_STIFFNESS_FACTOR_OF_SHEAR_Z_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_STIFFNESS_FACTOR_OF_TORSION_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_STIFFNESS_FACTOR_OF_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_STIFFNESS_FACTOR_OF_TOTAL_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
    STEEL_STRUCTURE_CSA_STIFFNESS_FACTOR_OF_SHEAR_Y_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
    STEEL_STRUCTURE_CSA_STIFFNESS_FACTOR_OF_SHEAR_Z_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
    STEEL_STRUCTURE_CSA_STIFFNESS_FACTOR_OF_TORSION_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
    STEEL_STRUCTURE_CSA_FACTOR_OF_AXIAL_STIFFNESS_ENABLE_FIELD_NUMBER: _ClassVar[int]
    STEEL_STRUCTURE_CSA_FACTOR_OF_BENDING_Y_STIFFNESS_ENABLE_FIELD_NUMBER: _ClassVar[int]
    STEEL_STRUCTURE_CSA_FACTOR_OF_BENDING_Z_STIFFNESS_ENABLE_FIELD_NUMBER: _ClassVar[int]
    STEEL_STRUCTURE_CSA_FACTOR_OF_SHEAR_Y_STIFFNESS_ENABLE_FIELD_NUMBER: _ClassVar[int]
    STEEL_STRUCTURE_CSA_FACTOR_OF_SHEAR_Z_STIFFNESS_ENABLE_FIELD_NUMBER: _ClassVar[int]
    STEEL_STRUCTURE_CSA_STIFFNESS_FACTOR_OF_TORSION_STIFFNESS_ENABLE_FIELD_NUMBER: _ClassVar[int]
    STEEL_STRUCTURE_CSA_DETERMINE_TAU_B_FIELD_NUMBER: _ClassVar[int]
    STEEL_STRUCTURE_GB_DIRECT_METHOD_ENABLED_FIELD_NUMBER: _ClassVar[int]
    STEEL_STRUCTURE_DETERMINE_TAU_B_FIELD_NUMBER: _ClassVar[int]
    STEEL_STRUCTURE_DESIGN_METHOD_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_STRUCTURE_COMPONENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_STRUCTURE_MODIFICATION_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: MemberStiffnessModificationType
    user_defined_name_enabled: bool
    name: str
    factor_of_axial_stiffness: float
    factor_of_bending_y_stiffness: float
    factor_of_bending_z_stiffness: float
    partial_stiffness_factor_of_shear_y_stiffness: float
    partial_stiffness_factor_of_shear_z_stiffness: float
    partial_stiffness_factor_of_torsion_stiffness: float
    partial_stiffness_factor_of_weight: float
    total_stiffness_factor_of_total_stiffness: float
    steel_structure_csa_stiffness_factor_of_shear_y_stiffness: float
    steel_structure_csa_stiffness_factor_of_shear_z_stiffness: float
    steel_structure_csa_stiffness_factor_of_torsion_stiffness: float
    steel_structure_csa_factor_of_axial_stiffness_enable: bool
    steel_structure_csa_factor_of_bending_y_stiffness_enable: bool
    steel_structure_csa_factor_of_bending_z_stiffness_enable: bool
    steel_structure_csa_factor_of_shear_y_stiffness_enable: bool
    steel_structure_csa_factor_of_shear_z_stiffness_enable: bool
    steel_structure_csa_stiffness_factor_of_torsion_stiffness_enable: bool
    steel_structure_csa_determine_tau_b: MemberStiffnessModificationSteelStructureCsaDetermineTauB
    steel_structure_gb_direct_method_enabled: bool
    steel_structure_determine_tau_b: MemberStiffnessModificationSteelStructureDetermineTauB
    steel_structure_design_method: MemberStiffnessModificationSteelStructureDesignMethod
    concrete_structure_component_type: MemberStiffnessModificationConcreteStructureComponentType
    assigned_to_structure_modification: _containers.RepeatedScalarFieldContainer[int]
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[MemberStiffnessModificationType, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., factor_of_axial_stiffness: _Optional[float] = ..., factor_of_bending_y_stiffness: _Optional[float] = ..., factor_of_bending_z_stiffness: _Optional[float] = ..., partial_stiffness_factor_of_shear_y_stiffness: _Optional[float] = ..., partial_stiffness_factor_of_shear_z_stiffness: _Optional[float] = ..., partial_stiffness_factor_of_torsion_stiffness: _Optional[float] = ..., partial_stiffness_factor_of_weight: _Optional[float] = ..., total_stiffness_factor_of_total_stiffness: _Optional[float] = ..., steel_structure_csa_stiffness_factor_of_shear_y_stiffness: _Optional[float] = ..., steel_structure_csa_stiffness_factor_of_shear_z_stiffness: _Optional[float] = ..., steel_structure_csa_stiffness_factor_of_torsion_stiffness: _Optional[float] = ..., steel_structure_csa_factor_of_axial_stiffness_enable: bool = ..., steel_structure_csa_factor_of_bending_y_stiffness_enable: bool = ..., steel_structure_csa_factor_of_bending_z_stiffness_enable: bool = ..., steel_structure_csa_factor_of_shear_y_stiffness_enable: bool = ..., steel_structure_csa_factor_of_shear_z_stiffness_enable: bool = ..., steel_structure_csa_stiffness_factor_of_torsion_stiffness_enable: bool = ..., steel_structure_csa_determine_tau_b: _Optional[_Union[MemberStiffnessModificationSteelStructureCsaDetermineTauB, str]] = ..., steel_structure_gb_direct_method_enabled: bool = ..., steel_structure_determine_tau_b: _Optional[_Union[MemberStiffnessModificationSteelStructureDetermineTauB, str]] = ..., steel_structure_design_method: _Optional[_Union[MemberStiffnessModificationSteelStructureDesignMethod, str]] = ..., concrete_structure_component_type: _Optional[_Union[MemberStiffnessModificationConcreteStructureComponentType, str]] = ..., assigned_to_structure_modification: _Optional[_Iterable[int]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
