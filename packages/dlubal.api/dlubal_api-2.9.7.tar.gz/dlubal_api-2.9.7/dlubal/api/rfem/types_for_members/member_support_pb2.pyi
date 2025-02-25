from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberSupportNonlinearityTranslationalZ(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Z_NONLINEARITY_NONE: _ClassVar[MemberSupportNonlinearityTranslationalZ]
    MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Z_NONLINEARITY_FAILURE_IF_NEGATIVE_CONTACT_STRESS_Z: _ClassVar[MemberSupportNonlinearityTranslationalZ]
    MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Z_NONLINEARITY_FAILURE_IF_POSITIVE_CONTACT_STRESS_Z: _ClassVar[MemberSupportNonlinearityTranslationalZ]
    MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Z_NONLINEARITY_ROTATION_RESTRAINT_ABOUT_X: _ClassVar[MemberSupportNonlinearityTranslationalZ]
    MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Z_NONLINEARITY_SHEAR_PANEL_IN_Y: _ClassVar[MemberSupportNonlinearityTranslationalZ]
    MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Z_NONLINEARITY_SHEAR_PANEL_IN_Z: _ClassVar[MemberSupportNonlinearityTranslationalZ]

class MemberSupportNonlinearityRotationalX(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_SUPPORT_NONLINEARITY_ROTATIONAL_X_NONLINEARITY_NONE: _ClassVar[MemberSupportNonlinearityRotationalX]
    MEMBER_SUPPORT_NONLINEARITY_ROTATIONAL_X_NONLINEARITY_FAILURE_IF_NEGATIVE_CONTACT_STRESS_Z: _ClassVar[MemberSupportNonlinearityRotationalX]
    MEMBER_SUPPORT_NONLINEARITY_ROTATIONAL_X_NONLINEARITY_FAILURE_IF_POSITIVE_CONTACT_STRESS_Z: _ClassVar[MemberSupportNonlinearityRotationalX]
    MEMBER_SUPPORT_NONLINEARITY_ROTATIONAL_X_NONLINEARITY_ROTATION_RESTRAINT_ABOUT_X: _ClassVar[MemberSupportNonlinearityRotationalX]
    MEMBER_SUPPORT_NONLINEARITY_ROTATIONAL_X_NONLINEARITY_SHEAR_PANEL_IN_Y: _ClassVar[MemberSupportNonlinearityRotationalX]
    MEMBER_SUPPORT_NONLINEARITY_ROTATIONAL_X_NONLINEARITY_SHEAR_PANEL_IN_Z: _ClassVar[MemberSupportNonlinearityRotationalX]

class MemberSupportEccentricityCenter(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_SUPPORT_ECCENTRICITY_CENTER_OF_GRAVITY: _ClassVar[MemberSupportEccentricityCenter]
    MEMBER_SUPPORT_ECCENTRICITY_NONE: _ClassVar[MemberSupportEccentricityCenter]
    MEMBER_SUPPORT_ECCENTRICITY_SHEAR_CENTER: _ClassVar[MemberSupportEccentricityCenter]

class MemberSupportEccentricityHorizontalAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_SUPPORT_ECCENTRICITY_HORIZONTAL_ALIGNMENT_LEFT: _ClassVar[MemberSupportEccentricityHorizontalAlignment]
    MEMBER_SUPPORT_ECCENTRICITY_HORIZONTAL_ALIGNMENT_CENTER: _ClassVar[MemberSupportEccentricityHorizontalAlignment]
    MEMBER_SUPPORT_ECCENTRICITY_HORIZONTAL_ALIGNMENT_NONE: _ClassVar[MemberSupportEccentricityHorizontalAlignment]
    MEMBER_SUPPORT_ECCENTRICITY_HORIZONTAL_ALIGNMENT_RIGHT: _ClassVar[MemberSupportEccentricityHorizontalAlignment]

class MemberSupportEccentricityVerticalAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_SUPPORT_ECCENTRICITY_VERTICAL_ALIGNMENT_TOP: _ClassVar[MemberSupportEccentricityVerticalAlignment]
    MEMBER_SUPPORT_ECCENTRICITY_VERTICAL_ALIGNMENT_BOTTOM: _ClassVar[MemberSupportEccentricityVerticalAlignment]
    MEMBER_SUPPORT_ECCENTRICITY_VERTICAL_ALIGNMENT_CENTER: _ClassVar[MemberSupportEccentricityVerticalAlignment]
    MEMBER_SUPPORT_ECCENTRICITY_VERTICAL_ALIGNMENT_NONE: _ClassVar[MemberSupportEccentricityVerticalAlignment]

class MemberSupportNonlinearityTranslationalY(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Y_NONLINEARITY_NONE: _ClassVar[MemberSupportNonlinearityTranslationalY]
    MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Y_NONLINEARITY_FAILURE_IF_NEGATIVE_CONTACT_STRESS_Z: _ClassVar[MemberSupportNonlinearityTranslationalY]
    MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Y_NONLINEARITY_FAILURE_IF_POSITIVE_CONTACT_STRESS_Z: _ClassVar[MemberSupportNonlinearityTranslationalY]
    MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Y_NONLINEARITY_ROTATION_RESTRAINT_ABOUT_X: _ClassVar[MemberSupportNonlinearityTranslationalY]
    MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Y_NONLINEARITY_SHEAR_PANEL_IN_Y: _ClassVar[MemberSupportNonlinearityTranslationalY]
    MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Y_NONLINEARITY_SHEAR_PANEL_IN_Z: _ClassVar[MemberSupportNonlinearityTranslationalY]
MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Z_NONLINEARITY_NONE: MemberSupportNonlinearityTranslationalZ
MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Z_NONLINEARITY_FAILURE_IF_NEGATIVE_CONTACT_STRESS_Z: MemberSupportNonlinearityTranslationalZ
MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Z_NONLINEARITY_FAILURE_IF_POSITIVE_CONTACT_STRESS_Z: MemberSupportNonlinearityTranslationalZ
MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Z_NONLINEARITY_ROTATION_RESTRAINT_ABOUT_X: MemberSupportNonlinearityTranslationalZ
MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Z_NONLINEARITY_SHEAR_PANEL_IN_Y: MemberSupportNonlinearityTranslationalZ
MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Z_NONLINEARITY_SHEAR_PANEL_IN_Z: MemberSupportNonlinearityTranslationalZ
MEMBER_SUPPORT_NONLINEARITY_ROTATIONAL_X_NONLINEARITY_NONE: MemberSupportNonlinearityRotationalX
MEMBER_SUPPORT_NONLINEARITY_ROTATIONAL_X_NONLINEARITY_FAILURE_IF_NEGATIVE_CONTACT_STRESS_Z: MemberSupportNonlinearityRotationalX
MEMBER_SUPPORT_NONLINEARITY_ROTATIONAL_X_NONLINEARITY_FAILURE_IF_POSITIVE_CONTACT_STRESS_Z: MemberSupportNonlinearityRotationalX
MEMBER_SUPPORT_NONLINEARITY_ROTATIONAL_X_NONLINEARITY_ROTATION_RESTRAINT_ABOUT_X: MemberSupportNonlinearityRotationalX
MEMBER_SUPPORT_NONLINEARITY_ROTATIONAL_X_NONLINEARITY_SHEAR_PANEL_IN_Y: MemberSupportNonlinearityRotationalX
MEMBER_SUPPORT_NONLINEARITY_ROTATIONAL_X_NONLINEARITY_SHEAR_PANEL_IN_Z: MemberSupportNonlinearityRotationalX
MEMBER_SUPPORT_ECCENTRICITY_CENTER_OF_GRAVITY: MemberSupportEccentricityCenter
MEMBER_SUPPORT_ECCENTRICITY_NONE: MemberSupportEccentricityCenter
MEMBER_SUPPORT_ECCENTRICITY_SHEAR_CENTER: MemberSupportEccentricityCenter
MEMBER_SUPPORT_ECCENTRICITY_HORIZONTAL_ALIGNMENT_LEFT: MemberSupportEccentricityHorizontalAlignment
MEMBER_SUPPORT_ECCENTRICITY_HORIZONTAL_ALIGNMENT_CENTER: MemberSupportEccentricityHorizontalAlignment
MEMBER_SUPPORT_ECCENTRICITY_HORIZONTAL_ALIGNMENT_NONE: MemberSupportEccentricityHorizontalAlignment
MEMBER_SUPPORT_ECCENTRICITY_HORIZONTAL_ALIGNMENT_RIGHT: MemberSupportEccentricityHorizontalAlignment
MEMBER_SUPPORT_ECCENTRICITY_VERTICAL_ALIGNMENT_TOP: MemberSupportEccentricityVerticalAlignment
MEMBER_SUPPORT_ECCENTRICITY_VERTICAL_ALIGNMENT_BOTTOM: MemberSupportEccentricityVerticalAlignment
MEMBER_SUPPORT_ECCENTRICITY_VERTICAL_ALIGNMENT_CENTER: MemberSupportEccentricityVerticalAlignment
MEMBER_SUPPORT_ECCENTRICITY_VERTICAL_ALIGNMENT_NONE: MemberSupportEccentricityVerticalAlignment
MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Y_NONLINEARITY_NONE: MemberSupportNonlinearityTranslationalY
MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Y_NONLINEARITY_FAILURE_IF_NEGATIVE_CONTACT_STRESS_Z: MemberSupportNonlinearityTranslationalY
MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Y_NONLINEARITY_FAILURE_IF_POSITIVE_CONTACT_STRESS_Z: MemberSupportNonlinearityTranslationalY
MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Y_NONLINEARITY_ROTATION_RESTRAINT_ABOUT_X: MemberSupportNonlinearityTranslationalY
MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Y_NONLINEARITY_SHEAR_PANEL_IN_Y: MemberSupportNonlinearityTranslationalY
MEMBER_SUPPORT_NONLINEARITY_TRANSLATIONAL_Y_NONLINEARITY_SHEAR_PANEL_IN_Z: MemberSupportNonlinearityTranslationalY

class MemberSupport(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "members", "member_sets", "spring_translation", "spring_rotation", "spring_translation_x", "spring_translation_y", "minimal_and_maximal_spring_translation_y", "spring_translation_z", "spring_shear", "spring_shear_x", "spring_shear_y", "spring_shear_z", "minimal_and_maximal_spring_rotation", "nonlinearity_translational_z", "support_dimensions_enabled", "eccentricity_enabled", "support_width_y", "support_width_z", "eccentricity_offset_y", "eccentricity_offset_z", "member_shear_panel_z", "nonlinearity_rotational_x", "member_rotational_restraint", "comment", "is_generated", "eccentricity_center", "eccentricity_horizontal_alignment", "eccentricity_vertical_alignment", "member_shear_panel_y", "minimal_and_maximal_spring_translation_z", "nonlinearity_translational_y", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    SPRING_TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    SPRING_ROTATION_FIELD_NUMBER: _ClassVar[int]
    SPRING_TRANSLATION_X_FIELD_NUMBER: _ClassVar[int]
    SPRING_TRANSLATION_Y_FIELD_NUMBER: _ClassVar[int]
    MINIMAL_AND_MAXIMAL_SPRING_TRANSLATION_Y_FIELD_NUMBER: _ClassVar[int]
    SPRING_TRANSLATION_Z_FIELD_NUMBER: _ClassVar[int]
    SPRING_SHEAR_FIELD_NUMBER: _ClassVar[int]
    SPRING_SHEAR_X_FIELD_NUMBER: _ClassVar[int]
    SPRING_SHEAR_Y_FIELD_NUMBER: _ClassVar[int]
    SPRING_SHEAR_Z_FIELD_NUMBER: _ClassVar[int]
    MINIMAL_AND_MAXIMAL_SPRING_ROTATION_FIELD_NUMBER: _ClassVar[int]
    NONLINEARITY_TRANSLATIONAL_Z_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_DIMENSIONS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_WIDTH_Y_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_WIDTH_Z_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_OFFSET_Y_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_OFFSET_Z_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SHEAR_PANEL_Z_FIELD_NUMBER: _ClassVar[int]
    NONLINEARITY_ROTATIONAL_X_FIELD_NUMBER: _ClassVar[int]
    MEMBER_ROTATIONAL_RESTRAINT_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_CENTER_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_HORIZONTAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_VERTICAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SHEAR_PANEL_Y_FIELD_NUMBER: _ClassVar[int]
    MINIMAL_AND_MAXIMAL_SPRING_TRANSLATION_Z_FIELD_NUMBER: _ClassVar[int]
    NONLINEARITY_TRANSLATIONAL_Y_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    members: _containers.RepeatedScalarFieldContainer[int]
    member_sets: _containers.RepeatedScalarFieldContainer[int]
    spring_translation: _common_pb2.Vector3d
    spring_rotation: float
    spring_translation_x: float
    spring_translation_y: float
    minimal_and_maximal_spring_translation_y: _containers.RepeatedScalarFieldContainer[int]
    spring_translation_z: float
    spring_shear: _common_pb2.Vector3d
    spring_shear_x: float
    spring_shear_y: float
    spring_shear_z: float
    minimal_and_maximal_spring_rotation: _containers.RepeatedScalarFieldContainer[int]
    nonlinearity_translational_z: MemberSupportNonlinearityTranslationalZ
    support_dimensions_enabled: bool
    eccentricity_enabled: bool
    support_width_y: float
    support_width_z: float
    eccentricity_offset_y: float
    eccentricity_offset_z: float
    member_shear_panel_z: int
    nonlinearity_rotational_x: MemberSupportNonlinearityRotationalX
    member_rotational_restraint: int
    comment: str
    is_generated: bool
    eccentricity_center: MemberSupportEccentricityCenter
    eccentricity_horizontal_alignment: MemberSupportEccentricityHorizontalAlignment
    eccentricity_vertical_alignment: MemberSupportEccentricityVerticalAlignment
    member_shear_panel_y: int
    minimal_and_maximal_spring_translation_z: _containers.RepeatedScalarFieldContainer[int]
    nonlinearity_translational_y: MemberSupportNonlinearityTranslationalY
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., members: _Optional[_Iterable[int]] = ..., member_sets: _Optional[_Iterable[int]] = ..., spring_translation: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., spring_rotation: _Optional[float] = ..., spring_translation_x: _Optional[float] = ..., spring_translation_y: _Optional[float] = ..., minimal_and_maximal_spring_translation_y: _Optional[_Iterable[int]] = ..., spring_translation_z: _Optional[float] = ..., spring_shear: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., spring_shear_x: _Optional[float] = ..., spring_shear_y: _Optional[float] = ..., spring_shear_z: _Optional[float] = ..., minimal_and_maximal_spring_rotation: _Optional[_Iterable[int]] = ..., nonlinearity_translational_z: _Optional[_Union[MemberSupportNonlinearityTranslationalZ, str]] = ..., support_dimensions_enabled: bool = ..., eccentricity_enabled: bool = ..., support_width_y: _Optional[float] = ..., support_width_z: _Optional[float] = ..., eccentricity_offset_y: _Optional[float] = ..., eccentricity_offset_z: _Optional[float] = ..., member_shear_panel_z: _Optional[int] = ..., nonlinearity_rotational_x: _Optional[_Union[MemberSupportNonlinearityRotationalX, str]] = ..., member_rotational_restraint: _Optional[int] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., eccentricity_center: _Optional[_Union[MemberSupportEccentricityCenter, str]] = ..., eccentricity_horizontal_alignment: _Optional[_Union[MemberSupportEccentricityHorizontalAlignment, str]] = ..., eccentricity_vertical_alignment: _Optional[_Union[MemberSupportEccentricityVerticalAlignment, str]] = ..., member_shear_panel_y: _Optional[int] = ..., minimal_and_maximal_spring_translation_z: _Optional[_Iterable[int]] = ..., nonlinearity_translational_y: _Optional[_Union[MemberSupportNonlinearityTranslationalY, str]] = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
