from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SurfaceSupportNonlinearity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SUPPORT_NONLINEARITY_NONE: _ClassVar[SurfaceSupportNonlinearity]
    SURFACE_SUPPORT_NONLINEARITY_FAILURE_IF_NEGATIVE_CONTACT_STRESS_Z: _ClassVar[SurfaceSupportNonlinearity]
    SURFACE_SUPPORT_NONLINEARITY_FAILURE_IF_POSITIVE_CONTACT_STRESS_Z: _ClassVar[SurfaceSupportNonlinearity]

class SurfaceSupportNegativeNonlinearityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SUPPORT_NEGATIVE_NONLINEARITY_TYPE_BASIC_UNIDIRECTIONAL_ACTION: _ClassVar[SurfaceSupportNegativeNonlinearityType]
    SURFACE_SUPPORT_NEGATIVE_NONLINEARITY_TYPE_FRICTION_PLANE_XY: _ClassVar[SurfaceSupportNegativeNonlinearityType]
    SURFACE_SUPPORT_NEGATIVE_NONLINEARITY_TYPE_YIELDING_CONTACT_STRESS_SIGMA_Z: _ClassVar[SurfaceSupportNegativeNonlinearityType]

class SurfaceSupportPositiveNonlinearityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURFACE_SUPPORT_POSITIVE_NONLINEARITY_TYPE_BASIC_UNIDIRECTIONAL_ACTION: _ClassVar[SurfaceSupportPositiveNonlinearityType]
    SURFACE_SUPPORT_POSITIVE_NONLINEARITY_TYPE_FRICTION_PLANE_XY: _ClassVar[SurfaceSupportPositiveNonlinearityType]
    SURFACE_SUPPORT_POSITIVE_NONLINEARITY_TYPE_YIELDING_CONTACT_STRESS_SIGMA_Z: _ClassVar[SurfaceSupportPositiveNonlinearityType]
SURFACE_SUPPORT_NONLINEARITY_NONE: SurfaceSupportNonlinearity
SURFACE_SUPPORT_NONLINEARITY_FAILURE_IF_NEGATIVE_CONTACT_STRESS_Z: SurfaceSupportNonlinearity
SURFACE_SUPPORT_NONLINEARITY_FAILURE_IF_POSITIVE_CONTACT_STRESS_Z: SurfaceSupportNonlinearity
SURFACE_SUPPORT_NEGATIVE_NONLINEARITY_TYPE_BASIC_UNIDIRECTIONAL_ACTION: SurfaceSupportNegativeNonlinearityType
SURFACE_SUPPORT_NEGATIVE_NONLINEARITY_TYPE_FRICTION_PLANE_XY: SurfaceSupportNegativeNonlinearityType
SURFACE_SUPPORT_NEGATIVE_NONLINEARITY_TYPE_YIELDING_CONTACT_STRESS_SIGMA_Z: SurfaceSupportNegativeNonlinearityType
SURFACE_SUPPORT_POSITIVE_NONLINEARITY_TYPE_BASIC_UNIDIRECTIONAL_ACTION: SurfaceSupportPositiveNonlinearityType
SURFACE_SUPPORT_POSITIVE_NONLINEARITY_TYPE_FRICTION_PLANE_XY: SurfaceSupportPositiveNonlinearityType
SURFACE_SUPPORT_POSITIVE_NONLINEARITY_TYPE_YIELDING_CONTACT_STRESS_SIGMA_Z: SurfaceSupportPositiveNonlinearityType

class SurfaceSupport(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "surfaces", "translation", "translation_x", "translation_y", "translation_z", "shear_xz", "shear_yz", "nonlinearity", "negative_nonlinearity_type", "positive_nonlinearity_type", "negative_friction_coefficient", "positive_friction_coefficient", "negative_contact_stress", "positive_contact_stress", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURFACES_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_X_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_Y_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_Z_FIELD_NUMBER: _ClassVar[int]
    SHEAR_XZ_FIELD_NUMBER: _ClassVar[int]
    SHEAR_YZ_FIELD_NUMBER: _ClassVar[int]
    NONLINEARITY_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_NONLINEARITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSITIVE_NONLINEARITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_FRICTION_COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
    POSITIVE_FRICTION_COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_CONTACT_STRESS_FIELD_NUMBER: _ClassVar[int]
    POSITIVE_CONTACT_STRESS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    surfaces: _containers.RepeatedScalarFieldContainer[int]
    translation: _common_pb2.Vector3d
    translation_x: float
    translation_y: float
    translation_z: float
    shear_xz: float
    shear_yz: float
    nonlinearity: SurfaceSupportNonlinearity
    negative_nonlinearity_type: SurfaceSupportNegativeNonlinearityType
    positive_nonlinearity_type: SurfaceSupportPositiveNonlinearityType
    negative_friction_coefficient: float
    positive_friction_coefficient: float
    negative_contact_stress: float
    positive_contact_stress: float
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., surfaces: _Optional[_Iterable[int]] = ..., translation: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., translation_x: _Optional[float] = ..., translation_y: _Optional[float] = ..., translation_z: _Optional[float] = ..., shear_xz: _Optional[float] = ..., shear_yz: _Optional[float] = ..., nonlinearity: _Optional[_Union[SurfaceSupportNonlinearity, str]] = ..., negative_nonlinearity_type: _Optional[_Union[SurfaceSupportNegativeNonlinearityType, str]] = ..., positive_nonlinearity_type: _Optional[_Union[SurfaceSupportPositiveNonlinearityType, str]] = ..., negative_friction_coefficient: _Optional[float] = ..., positive_friction_coefficient: _Optional[float] = ..., negative_contact_stress: _Optional[float] = ..., positive_contact_stress: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
