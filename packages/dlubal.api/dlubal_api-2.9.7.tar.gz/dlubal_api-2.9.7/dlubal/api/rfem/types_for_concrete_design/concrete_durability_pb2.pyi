from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConcreteDurabilityNoRiskOfCorrosionOrAttack(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_NO_RISK_OF_CORROSION_OR_ATTACK_VERY_DRY: _ClassVar[ConcreteDurabilityNoRiskOfCorrosionOrAttack]

class ConcreteDurabilityCorrosionInducedByCarbonation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CARBONATION_DRY_OR_PERMANENTLY_WET: _ClassVar[ConcreteDurabilityCorrosionInducedByCarbonation]
    CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CARBONATION_CYCLIC_WET_AND_DRY: _ClassVar[ConcreteDurabilityCorrosionInducedByCarbonation]
    CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CARBONATION_MODERATE_HUMIDITY: _ClassVar[ConcreteDurabilityCorrosionInducedByCarbonation]
    CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CARBONATION_WET_RARELY_DRY: _ClassVar[ConcreteDurabilityCorrosionInducedByCarbonation]

class ConcreteDurabilityCorrosionInducedByChlorides(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CHLORIDES_MODERATE_HUMIDITY: _ClassVar[ConcreteDurabilityCorrosionInducedByChlorides]
    CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CHLORIDES_CYCLIC_WET_AND_DRY: _ClassVar[ConcreteDurabilityCorrosionInducedByChlorides]
    CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CHLORIDES_WET_RARELY_DRY: _ClassVar[ConcreteDurabilityCorrosionInducedByChlorides]

class ConcreteDurabilityCorrosionInducedByChloridesFromSeaWater(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CHLORIDES_FROM_SEA_WATER_EXPOSED_TO_AIRBORNE_SALT: _ClassVar[ConcreteDurabilityCorrosionInducedByChloridesFromSeaWater]
    CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CHLORIDES_FROM_SEA_WATER_PERMANENTLY_SUBMERGED: _ClassVar[ConcreteDurabilityCorrosionInducedByChloridesFromSeaWater]
    CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CHLORIDES_FROM_SEA_WATER_TIDAL_SPLASH_AND_SPRAY_ZONES: _ClassVar[ConcreteDurabilityCorrosionInducedByChloridesFromSeaWater]

class ConcreteDurabilityFreezeThawAttack(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_FREEZE_THAW_ATTACK_MODERATE_WATER_SATURATION_NO_DEICING: _ClassVar[ConcreteDurabilityFreezeThawAttack]
    CONCRETE_DURABILITY_FREEZE_THAW_ATTACK_HIGH_WATER_SATURATION_DEICING: _ClassVar[ConcreteDurabilityFreezeThawAttack]
    CONCRETE_DURABILITY_FREEZE_THAW_ATTACK_HIGH_WATER_SATURATION_NO_DEICING: _ClassVar[ConcreteDurabilityFreezeThawAttack]
    CONCRETE_DURABILITY_FREEZE_THAW_ATTACK_MODERATE_WATER_SATURATION_DEICING: _ClassVar[ConcreteDurabilityFreezeThawAttack]

class ConcreteDurabilityChemicalAttack(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_CHEMICAL_ATTACK_SLIGHTLY_AGGRESSIVE: _ClassVar[ConcreteDurabilityChemicalAttack]
    CONCRETE_DURABILITY_CHEMICAL_ATTACK_HIGHLY_AGGRESSIVE: _ClassVar[ConcreteDurabilityChemicalAttack]
    CONCRETE_DURABILITY_CHEMICAL_ATTACK_MODERATELY_AGGRESSIVE: _ClassVar[ConcreteDurabilityChemicalAttack]

class ConcreteDurabilityConcreteCorrosionInducedByWear(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_CONCRETE_CORROSION_INDUCED_BY_WEAR_MODERATE: _ClassVar[ConcreteDurabilityConcreteCorrosionInducedByWear]
    CONCRETE_DURABILITY_CONCRETE_CORROSION_INDUCED_BY_WEAR_HIGH: _ClassVar[ConcreteDurabilityConcreteCorrosionInducedByWear]
    CONCRETE_DURABILITY_CONCRETE_CORROSION_INDUCED_BY_WEAR_VERY_HIGH: _ClassVar[ConcreteDurabilityConcreteCorrosionInducedByWear]

class ConcreteDurabilityStructuralClassType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_STRUCTURAL_CLASS_TYPE_STANDARD: _ClassVar[ConcreteDurabilityStructuralClassType]
    CONCRETE_DURABILITY_STRUCTURAL_CLASS_TYPE_DEFINED: _ClassVar[ConcreteDurabilityStructuralClassType]

class ConcreteDurabilityUserdefinedStructuralClass(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_UNKNOWN: _ClassVar[ConcreteDurabilityUserdefinedStructuralClass]
    CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_S1: _ClassVar[ConcreteDurabilityUserdefinedStructuralClass]
    CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_S2: _ClassVar[ConcreteDurabilityUserdefinedStructuralClass]
    CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_S3: _ClassVar[ConcreteDurabilityUserdefinedStructuralClass]
    CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_S4: _ClassVar[ConcreteDurabilityUserdefinedStructuralClass]
    CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_S5: _ClassVar[ConcreteDurabilityUserdefinedStructuralClass]
    CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_S6: _ClassVar[ConcreteDurabilityUserdefinedStructuralClass]

class ConcreteDurabilityDesignWorkingLife(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_50_YEARS: _ClassVar[ConcreteDurabilityDesignWorkingLife]
    CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_100_YEARS: _ClassVar[ConcreteDurabilityDesignWorkingLife]
    CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_20_YEARS: _ClassVar[ConcreteDurabilityDesignWorkingLife]
    CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_25_YEARS: _ClassVar[ConcreteDurabilityDesignWorkingLife]
    CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_30_YEARS: _ClassVar[ConcreteDurabilityDesignWorkingLife]
    CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_75_YEARS: _ClassVar[ConcreteDurabilityDesignWorkingLife]
    CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_80_YEARS: _ClassVar[ConcreteDurabilityDesignWorkingLife]

class ConcreteDurabilityMaximumEquivalentWaterToCementRatio(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_350: _ClassVar[ConcreteDurabilityMaximumEquivalentWaterToCementRatio]
    CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_000: _ClassVar[ConcreteDurabilityMaximumEquivalentWaterToCementRatio]
    CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_400: _ClassVar[ConcreteDurabilityMaximumEquivalentWaterToCementRatio]
    CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_450: _ClassVar[ConcreteDurabilityMaximumEquivalentWaterToCementRatio]
    CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_500: _ClassVar[ConcreteDurabilityMaximumEquivalentWaterToCementRatio]
    CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_550: _ClassVar[ConcreteDurabilityMaximumEquivalentWaterToCementRatio]
    CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_600: _ClassVar[ConcreteDurabilityMaximumEquivalentWaterToCementRatio]
    CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_900: _ClassVar[ConcreteDurabilityMaximumEquivalentWaterToCementRatio]

class ConcreteDurabilityIncreaseOfMinimumConcreteCoverType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_INCREASE_OF_MINIMUM_CONCRETE_COVER_TYPE_STANDARD: _ClassVar[ConcreteDurabilityIncreaseOfMinimumConcreteCoverType]
    CONCRETE_DURABILITY_INCREASE_OF_MINIMUM_CONCRETE_COVER_TYPE_DEFINED: _ClassVar[ConcreteDurabilityIncreaseOfMinimumConcreteCoverType]

class ConcreteDurabilityStainlessSteelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_STAINLESS_STEEL_TYPE_STANDARD: _ClassVar[ConcreteDurabilityStainlessSteelType]
    CONCRETE_DURABILITY_STAINLESS_STEEL_TYPE_DEFINED: _ClassVar[ConcreteDurabilityStainlessSteelType]

class ConcreteDurabilityAdditionalProtectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_ADDITIONAL_PROTECTION_TYPE_STANDARD: _ClassVar[ConcreteDurabilityAdditionalProtectionType]
    CONCRETE_DURABILITY_ADDITIONAL_PROTECTION_TYPE_DEFINED: _ClassVar[ConcreteDurabilityAdditionalProtectionType]

class ConcreteDurabilityAllowanceOfDeviationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_ALLOWANCE_OF_DEVIATION_TYPE_STANDARD: _ClassVar[ConcreteDurabilityAllowanceOfDeviationType]
    CONCRETE_DURABILITY_ALLOWANCE_OF_DEVIATION_TYPE_DEFINED: _ClassVar[ConcreteDurabilityAllowanceOfDeviationType]

class ConcreteDurabilityConcreteCast(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONCRETE_DURABILITY_CONCRETE_CAST_AGAINST_PREPARED_GROUND: _ClassVar[ConcreteDurabilityConcreteCast]
    CONCRETE_DURABILITY_CONCRETE_CAST_DIRECTLY_AGAINST_SOIL: _ClassVar[ConcreteDurabilityConcreteCast]
CONCRETE_DURABILITY_NO_RISK_OF_CORROSION_OR_ATTACK_VERY_DRY: ConcreteDurabilityNoRiskOfCorrosionOrAttack
CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CARBONATION_DRY_OR_PERMANENTLY_WET: ConcreteDurabilityCorrosionInducedByCarbonation
CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CARBONATION_CYCLIC_WET_AND_DRY: ConcreteDurabilityCorrosionInducedByCarbonation
CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CARBONATION_MODERATE_HUMIDITY: ConcreteDurabilityCorrosionInducedByCarbonation
CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CARBONATION_WET_RARELY_DRY: ConcreteDurabilityCorrosionInducedByCarbonation
CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CHLORIDES_MODERATE_HUMIDITY: ConcreteDurabilityCorrosionInducedByChlorides
CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CHLORIDES_CYCLIC_WET_AND_DRY: ConcreteDurabilityCorrosionInducedByChlorides
CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CHLORIDES_WET_RARELY_DRY: ConcreteDurabilityCorrosionInducedByChlorides
CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CHLORIDES_FROM_SEA_WATER_EXPOSED_TO_AIRBORNE_SALT: ConcreteDurabilityCorrosionInducedByChloridesFromSeaWater
CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CHLORIDES_FROM_SEA_WATER_PERMANENTLY_SUBMERGED: ConcreteDurabilityCorrosionInducedByChloridesFromSeaWater
CONCRETE_DURABILITY_CORROSION_INDUCED_BY_CHLORIDES_FROM_SEA_WATER_TIDAL_SPLASH_AND_SPRAY_ZONES: ConcreteDurabilityCorrosionInducedByChloridesFromSeaWater
CONCRETE_DURABILITY_FREEZE_THAW_ATTACK_MODERATE_WATER_SATURATION_NO_DEICING: ConcreteDurabilityFreezeThawAttack
CONCRETE_DURABILITY_FREEZE_THAW_ATTACK_HIGH_WATER_SATURATION_DEICING: ConcreteDurabilityFreezeThawAttack
CONCRETE_DURABILITY_FREEZE_THAW_ATTACK_HIGH_WATER_SATURATION_NO_DEICING: ConcreteDurabilityFreezeThawAttack
CONCRETE_DURABILITY_FREEZE_THAW_ATTACK_MODERATE_WATER_SATURATION_DEICING: ConcreteDurabilityFreezeThawAttack
CONCRETE_DURABILITY_CHEMICAL_ATTACK_SLIGHTLY_AGGRESSIVE: ConcreteDurabilityChemicalAttack
CONCRETE_DURABILITY_CHEMICAL_ATTACK_HIGHLY_AGGRESSIVE: ConcreteDurabilityChemicalAttack
CONCRETE_DURABILITY_CHEMICAL_ATTACK_MODERATELY_AGGRESSIVE: ConcreteDurabilityChemicalAttack
CONCRETE_DURABILITY_CONCRETE_CORROSION_INDUCED_BY_WEAR_MODERATE: ConcreteDurabilityConcreteCorrosionInducedByWear
CONCRETE_DURABILITY_CONCRETE_CORROSION_INDUCED_BY_WEAR_HIGH: ConcreteDurabilityConcreteCorrosionInducedByWear
CONCRETE_DURABILITY_CONCRETE_CORROSION_INDUCED_BY_WEAR_VERY_HIGH: ConcreteDurabilityConcreteCorrosionInducedByWear
CONCRETE_DURABILITY_STRUCTURAL_CLASS_TYPE_STANDARD: ConcreteDurabilityStructuralClassType
CONCRETE_DURABILITY_STRUCTURAL_CLASS_TYPE_DEFINED: ConcreteDurabilityStructuralClassType
CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_UNKNOWN: ConcreteDurabilityUserdefinedStructuralClass
CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_S1: ConcreteDurabilityUserdefinedStructuralClass
CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_S2: ConcreteDurabilityUserdefinedStructuralClass
CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_S3: ConcreteDurabilityUserdefinedStructuralClass
CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_S4: ConcreteDurabilityUserdefinedStructuralClass
CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_S5: ConcreteDurabilityUserdefinedStructuralClass
CONCRETE_DURABILITY_USERDEFINED_STRUCTURAL_CLASS_S6: ConcreteDurabilityUserdefinedStructuralClass
CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_50_YEARS: ConcreteDurabilityDesignWorkingLife
CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_100_YEARS: ConcreteDurabilityDesignWorkingLife
CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_20_YEARS: ConcreteDurabilityDesignWorkingLife
CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_25_YEARS: ConcreteDurabilityDesignWorkingLife
CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_30_YEARS: ConcreteDurabilityDesignWorkingLife
CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_75_YEARS: ConcreteDurabilityDesignWorkingLife
CONCRETE_DURABILITY_DESIGN_WORKING_LIFE_80_YEARS: ConcreteDurabilityDesignWorkingLife
CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_350: ConcreteDurabilityMaximumEquivalentWaterToCementRatio
CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_000: ConcreteDurabilityMaximumEquivalentWaterToCementRatio
CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_400: ConcreteDurabilityMaximumEquivalentWaterToCementRatio
CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_450: ConcreteDurabilityMaximumEquivalentWaterToCementRatio
CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_500: ConcreteDurabilityMaximumEquivalentWaterToCementRatio
CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_550: ConcreteDurabilityMaximumEquivalentWaterToCementRatio
CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_600: ConcreteDurabilityMaximumEquivalentWaterToCementRatio
CONCRETE_DURABILITY_MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_0_900: ConcreteDurabilityMaximumEquivalentWaterToCementRatio
CONCRETE_DURABILITY_INCREASE_OF_MINIMUM_CONCRETE_COVER_TYPE_STANDARD: ConcreteDurabilityIncreaseOfMinimumConcreteCoverType
CONCRETE_DURABILITY_INCREASE_OF_MINIMUM_CONCRETE_COVER_TYPE_DEFINED: ConcreteDurabilityIncreaseOfMinimumConcreteCoverType
CONCRETE_DURABILITY_STAINLESS_STEEL_TYPE_STANDARD: ConcreteDurabilityStainlessSteelType
CONCRETE_DURABILITY_STAINLESS_STEEL_TYPE_DEFINED: ConcreteDurabilityStainlessSteelType
CONCRETE_DURABILITY_ADDITIONAL_PROTECTION_TYPE_STANDARD: ConcreteDurabilityAdditionalProtectionType
CONCRETE_DURABILITY_ADDITIONAL_PROTECTION_TYPE_DEFINED: ConcreteDurabilityAdditionalProtectionType
CONCRETE_DURABILITY_ALLOWANCE_OF_DEVIATION_TYPE_STANDARD: ConcreteDurabilityAllowanceOfDeviationType
CONCRETE_DURABILITY_ALLOWANCE_OF_DEVIATION_TYPE_DEFINED: ConcreteDurabilityAllowanceOfDeviationType
CONCRETE_DURABILITY_CONCRETE_CAST_AGAINST_PREPARED_GROUND: ConcreteDurabilityConcreteCast
CONCRETE_DURABILITY_CONCRETE_CAST_DIRECTLY_AGAINST_SOIL: ConcreteDurabilityConcreteCast

class ConcreteDurability(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "members", "member_sets", "surfaces", "no_risk_of_corrosion_or_attack_enabled", "no_risk_of_corrosion_or_attack", "corrosion_induced_by_carbonation_enabled", "corrosion_induced_by_carbonation", "corrosion_induced_by_chlorides_enabled", "corrosion_induced_by_chlorides", "corrosion_induced_by_chlorides_from_sea_water_enabled", "corrosion_induced_by_chlorides_from_sea_water", "freeze_thaw_attack_enabled", "freeze_thaw_attack", "chemical_attack_enabled", "chemical_attack", "concrete_corrosion_induced_by_wear_enabled", "concrete_corrosion_induced_by_wear", "structural_class_type", "userdefined_structural_class", "design_working_life", "increase_design_working_life_from_50_to_100_years_enabled", "position_of_reinforcement_not_affected_by_construction_process_enabled", "special_quality_control_of_production_enabled", "nature_of_binder_without_fly_ash_enabled", "air_entrainment_of_more_than_4_percent_enabled", "compact_coating_enabled", "adequate_cement_enabled", "maximum_equivalent_water_to_cement_ratio", "strength_class_of_the_concrete_enabled", "increase_of_minimum_concrete_cover_type", "increase_of_minimum_concrete_cover_factor", "stainless_steel_enabled", "stainless_steel_type", "stainless_steel_factor", "additional_protection_enabled", "additional_protection_type", "additional_protection_factor", "allowance_of_deviation_type", "userdefined_allowance_of_deviation_factor", "relaxed_quality_control_enabled", "concrete_cast_enabled", "concrete_cast", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    SURFACES_FIELD_NUMBER: _ClassVar[int]
    NO_RISK_OF_CORROSION_OR_ATTACK_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NO_RISK_OF_CORROSION_OR_ATTACK_FIELD_NUMBER: _ClassVar[int]
    CORROSION_INDUCED_BY_CARBONATION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CORROSION_INDUCED_BY_CARBONATION_FIELD_NUMBER: _ClassVar[int]
    CORROSION_INDUCED_BY_CHLORIDES_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CORROSION_INDUCED_BY_CHLORIDES_FIELD_NUMBER: _ClassVar[int]
    CORROSION_INDUCED_BY_CHLORIDES_FROM_SEA_WATER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CORROSION_INDUCED_BY_CHLORIDES_FROM_SEA_WATER_FIELD_NUMBER: _ClassVar[int]
    FREEZE_THAW_ATTACK_ENABLED_FIELD_NUMBER: _ClassVar[int]
    FREEZE_THAW_ATTACK_FIELD_NUMBER: _ClassVar[int]
    CHEMICAL_ATTACK_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CHEMICAL_ATTACK_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_CORROSION_INDUCED_BY_WEAR_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_CORROSION_INDUCED_BY_WEAR_FIELD_NUMBER: _ClassVar[int]
    STRUCTURAL_CLASS_TYPE_FIELD_NUMBER: _ClassVar[int]
    USERDEFINED_STRUCTURAL_CLASS_FIELD_NUMBER: _ClassVar[int]
    DESIGN_WORKING_LIFE_FIELD_NUMBER: _ClassVar[int]
    INCREASE_DESIGN_WORKING_LIFE_FROM_50_TO_100_YEARS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    POSITION_OF_REINFORCEMENT_NOT_AFFECTED_BY_CONSTRUCTION_PROCESS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_QUALITY_CONTROL_OF_PRODUCTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NATURE_OF_BINDER_WITHOUT_FLY_ASH_ENABLED_FIELD_NUMBER: _ClassVar[int]
    AIR_ENTRAINMENT_OF_MORE_THAN_4_PERCENT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    COMPACT_COATING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ADEQUATE_CEMENT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_EQUIVALENT_WATER_TO_CEMENT_RATIO_FIELD_NUMBER: _ClassVar[int]
    STRENGTH_CLASS_OF_THE_CONCRETE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    INCREASE_OF_MINIMUM_CONCRETE_COVER_TYPE_FIELD_NUMBER: _ClassVar[int]
    INCREASE_OF_MINIMUM_CONCRETE_COVER_FACTOR_FIELD_NUMBER: _ClassVar[int]
    STAINLESS_STEEL_ENABLED_FIELD_NUMBER: _ClassVar[int]
    STAINLESS_STEEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    STAINLESS_STEEL_FACTOR_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_PROTECTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_PROTECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_PROTECTION_FACTOR_FIELD_NUMBER: _ClassVar[int]
    ALLOWANCE_OF_DEVIATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    USERDEFINED_ALLOWANCE_OF_DEVIATION_FACTOR_FIELD_NUMBER: _ClassVar[int]
    RELAXED_QUALITY_CONTROL_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_CAST_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_CAST_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    members: _containers.RepeatedScalarFieldContainer[int]
    member_sets: _containers.RepeatedScalarFieldContainer[int]
    surfaces: _containers.RepeatedScalarFieldContainer[int]
    no_risk_of_corrosion_or_attack_enabled: bool
    no_risk_of_corrosion_or_attack: ConcreteDurabilityNoRiskOfCorrosionOrAttack
    corrosion_induced_by_carbonation_enabled: bool
    corrosion_induced_by_carbonation: ConcreteDurabilityCorrosionInducedByCarbonation
    corrosion_induced_by_chlorides_enabled: bool
    corrosion_induced_by_chlorides: ConcreteDurabilityCorrosionInducedByChlorides
    corrosion_induced_by_chlorides_from_sea_water_enabled: bool
    corrosion_induced_by_chlorides_from_sea_water: ConcreteDurabilityCorrosionInducedByChloridesFromSeaWater
    freeze_thaw_attack_enabled: bool
    freeze_thaw_attack: ConcreteDurabilityFreezeThawAttack
    chemical_attack_enabled: bool
    chemical_attack: ConcreteDurabilityChemicalAttack
    concrete_corrosion_induced_by_wear_enabled: bool
    concrete_corrosion_induced_by_wear: ConcreteDurabilityConcreteCorrosionInducedByWear
    structural_class_type: ConcreteDurabilityStructuralClassType
    userdefined_structural_class: ConcreteDurabilityUserdefinedStructuralClass
    design_working_life: ConcreteDurabilityDesignWorkingLife
    increase_design_working_life_from_50_to_100_years_enabled: bool
    position_of_reinforcement_not_affected_by_construction_process_enabled: bool
    special_quality_control_of_production_enabled: bool
    nature_of_binder_without_fly_ash_enabled: bool
    air_entrainment_of_more_than_4_percent_enabled: bool
    compact_coating_enabled: bool
    adequate_cement_enabled: bool
    maximum_equivalent_water_to_cement_ratio: ConcreteDurabilityMaximumEquivalentWaterToCementRatio
    strength_class_of_the_concrete_enabled: bool
    increase_of_minimum_concrete_cover_type: ConcreteDurabilityIncreaseOfMinimumConcreteCoverType
    increase_of_minimum_concrete_cover_factor: float
    stainless_steel_enabled: bool
    stainless_steel_type: ConcreteDurabilityStainlessSteelType
    stainless_steel_factor: float
    additional_protection_enabled: bool
    additional_protection_type: ConcreteDurabilityAdditionalProtectionType
    additional_protection_factor: float
    allowance_of_deviation_type: ConcreteDurabilityAllowanceOfDeviationType
    userdefined_allowance_of_deviation_factor: float
    relaxed_quality_control_enabled: bool
    concrete_cast_enabled: bool
    concrete_cast: ConcreteDurabilityConcreteCast
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., members: _Optional[_Iterable[int]] = ..., member_sets: _Optional[_Iterable[int]] = ..., surfaces: _Optional[_Iterable[int]] = ..., no_risk_of_corrosion_or_attack_enabled: bool = ..., no_risk_of_corrosion_or_attack: _Optional[_Union[ConcreteDurabilityNoRiskOfCorrosionOrAttack, str]] = ..., corrosion_induced_by_carbonation_enabled: bool = ..., corrosion_induced_by_carbonation: _Optional[_Union[ConcreteDurabilityCorrosionInducedByCarbonation, str]] = ..., corrosion_induced_by_chlorides_enabled: bool = ..., corrosion_induced_by_chlorides: _Optional[_Union[ConcreteDurabilityCorrosionInducedByChlorides, str]] = ..., corrosion_induced_by_chlorides_from_sea_water_enabled: bool = ..., corrosion_induced_by_chlorides_from_sea_water: _Optional[_Union[ConcreteDurabilityCorrosionInducedByChloridesFromSeaWater, str]] = ..., freeze_thaw_attack_enabled: bool = ..., freeze_thaw_attack: _Optional[_Union[ConcreteDurabilityFreezeThawAttack, str]] = ..., chemical_attack_enabled: bool = ..., chemical_attack: _Optional[_Union[ConcreteDurabilityChemicalAttack, str]] = ..., concrete_corrosion_induced_by_wear_enabled: bool = ..., concrete_corrosion_induced_by_wear: _Optional[_Union[ConcreteDurabilityConcreteCorrosionInducedByWear, str]] = ..., structural_class_type: _Optional[_Union[ConcreteDurabilityStructuralClassType, str]] = ..., userdefined_structural_class: _Optional[_Union[ConcreteDurabilityUserdefinedStructuralClass, str]] = ..., design_working_life: _Optional[_Union[ConcreteDurabilityDesignWorkingLife, str]] = ..., increase_design_working_life_from_50_to_100_years_enabled: bool = ..., position_of_reinforcement_not_affected_by_construction_process_enabled: bool = ..., special_quality_control_of_production_enabled: bool = ..., nature_of_binder_without_fly_ash_enabled: bool = ..., air_entrainment_of_more_than_4_percent_enabled: bool = ..., compact_coating_enabled: bool = ..., adequate_cement_enabled: bool = ..., maximum_equivalent_water_to_cement_ratio: _Optional[_Union[ConcreteDurabilityMaximumEquivalentWaterToCementRatio, str]] = ..., strength_class_of_the_concrete_enabled: bool = ..., increase_of_minimum_concrete_cover_type: _Optional[_Union[ConcreteDurabilityIncreaseOfMinimumConcreteCoverType, str]] = ..., increase_of_minimum_concrete_cover_factor: _Optional[float] = ..., stainless_steel_enabled: bool = ..., stainless_steel_type: _Optional[_Union[ConcreteDurabilityStainlessSteelType, str]] = ..., stainless_steel_factor: _Optional[float] = ..., additional_protection_enabled: bool = ..., additional_protection_type: _Optional[_Union[ConcreteDurabilityAdditionalProtectionType, str]] = ..., additional_protection_factor: _Optional[float] = ..., allowance_of_deviation_type: _Optional[_Union[ConcreteDurabilityAllowanceOfDeviationType, str]] = ..., userdefined_allowance_of_deviation_factor: _Optional[float] = ..., relaxed_quality_control_enabled: bool = ..., concrete_cast_enabled: bool = ..., concrete_cast: _Optional[_Union[ConcreteDurabilityConcreteCast, str]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
