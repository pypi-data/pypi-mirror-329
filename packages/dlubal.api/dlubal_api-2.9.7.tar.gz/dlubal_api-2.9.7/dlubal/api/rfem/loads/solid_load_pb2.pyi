from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SolidLoadLoadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_LOAD_LOAD_TYPE_UNKNOWN: _ClassVar[SolidLoadLoadType]
    SOLID_LOAD_LOAD_TYPE_BUOYANCY: _ClassVar[SolidLoadLoadType]
    SOLID_LOAD_LOAD_TYPE_FORCE: _ClassVar[SolidLoadLoadType]
    SOLID_LOAD_LOAD_TYPE_GAS: _ClassVar[SolidLoadLoadType]
    SOLID_LOAD_LOAD_TYPE_ROTARY_MOTION: _ClassVar[SolidLoadLoadType]
    SOLID_LOAD_LOAD_TYPE_STRAIN: _ClassVar[SolidLoadLoadType]
    SOLID_LOAD_LOAD_TYPE_TEMPERATURE: _ClassVar[SolidLoadLoadType]

class SolidLoadLoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_LOAD_LOAD_DISTRIBUTION_UNIFORM: _ClassVar[SolidLoadLoadDistribution]
    SOLID_LOAD_LOAD_DISTRIBUTION_LINEAR_IN_X: _ClassVar[SolidLoadLoadDistribution]
    SOLID_LOAD_LOAD_DISTRIBUTION_LINEAR_IN_Y: _ClassVar[SolidLoadLoadDistribution]
    SOLID_LOAD_LOAD_DISTRIBUTION_LINEAR_IN_Z: _ClassVar[SolidLoadLoadDistribution]

class SolidLoadLoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_LOAD_LOAD_DIRECTION_UNKNOWN: _ClassVar[SolidLoadLoadDirection]
    SOLID_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE: _ClassVar[SolidLoadLoadDirection]
    SOLID_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE: _ClassVar[SolidLoadLoadDirection]
    SOLID_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE: _ClassVar[SolidLoadLoadDirection]

class SolidLoadLoadDirectionOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_LOAD_LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_FORWARD: _ClassVar[SolidLoadLoadDirectionOrientation]
    SOLID_LOAD_LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_REVERSED: _ClassVar[SolidLoadLoadDirectionOrientation]

class SolidLoadAxisDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_LOAD_AXIS_DEFINITION_TYPE_TWO_POINTS: _ClassVar[SolidLoadAxisDefinitionType]
    SOLID_LOAD_AXIS_DEFINITION_TYPE_POINT_AND_AXIS: _ClassVar[SolidLoadAxisDefinitionType]

class SolidLoadAxisDefinitionAxis(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_LOAD_AXIS_DEFINITION_AXIS_X: _ClassVar[SolidLoadAxisDefinitionAxis]
    SOLID_LOAD_AXIS_DEFINITION_AXIS_Y: _ClassVar[SolidLoadAxisDefinitionAxis]
    SOLID_LOAD_AXIS_DEFINITION_AXIS_Z: _ClassVar[SolidLoadAxisDefinitionAxis]

class SolidLoadAxisDefinitionAxisOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_LOAD_AXIS_DEFINITION_AXIS_ORIENTATION_POSITIVE: _ClassVar[SolidLoadAxisDefinitionAxisOrientation]
    SOLID_LOAD_AXIS_DEFINITION_AXIS_ORIENTATION_NEGATIVE: _ClassVar[SolidLoadAxisDefinitionAxisOrientation]

class SolidLoadGasBehaviour(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOLID_LOAD_GAS_BEHAVIOUR_RESULTING_OVERPRESSURE: _ClassVar[SolidLoadGasBehaviour]
    SOLID_LOAD_GAS_BEHAVIOUR_OVERPRESSURE_INCREMENT: _ClassVar[SolidLoadGasBehaviour]
    SOLID_LOAD_GAS_BEHAVIOUR_RESULTING_VOLUME: _ClassVar[SolidLoadGasBehaviour]
    SOLID_LOAD_GAS_BEHAVIOUR_VOLUME_INCREMENT: _ClassVar[SolidLoadGasBehaviour]
SOLID_LOAD_LOAD_TYPE_UNKNOWN: SolidLoadLoadType
SOLID_LOAD_LOAD_TYPE_BUOYANCY: SolidLoadLoadType
SOLID_LOAD_LOAD_TYPE_FORCE: SolidLoadLoadType
SOLID_LOAD_LOAD_TYPE_GAS: SolidLoadLoadType
SOLID_LOAD_LOAD_TYPE_ROTARY_MOTION: SolidLoadLoadType
SOLID_LOAD_LOAD_TYPE_STRAIN: SolidLoadLoadType
SOLID_LOAD_LOAD_TYPE_TEMPERATURE: SolidLoadLoadType
SOLID_LOAD_LOAD_DISTRIBUTION_UNIFORM: SolidLoadLoadDistribution
SOLID_LOAD_LOAD_DISTRIBUTION_LINEAR_IN_X: SolidLoadLoadDistribution
SOLID_LOAD_LOAD_DISTRIBUTION_LINEAR_IN_Y: SolidLoadLoadDistribution
SOLID_LOAD_LOAD_DISTRIBUTION_LINEAR_IN_Z: SolidLoadLoadDistribution
SOLID_LOAD_LOAD_DIRECTION_UNKNOWN: SolidLoadLoadDirection
SOLID_LOAD_LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE: SolidLoadLoadDirection
SOLID_LOAD_LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE: SolidLoadLoadDirection
SOLID_LOAD_LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE: SolidLoadLoadDirection
SOLID_LOAD_LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_FORWARD: SolidLoadLoadDirectionOrientation
SOLID_LOAD_LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_REVERSED: SolidLoadLoadDirectionOrientation
SOLID_LOAD_AXIS_DEFINITION_TYPE_TWO_POINTS: SolidLoadAxisDefinitionType
SOLID_LOAD_AXIS_DEFINITION_TYPE_POINT_AND_AXIS: SolidLoadAxisDefinitionType
SOLID_LOAD_AXIS_DEFINITION_AXIS_X: SolidLoadAxisDefinitionAxis
SOLID_LOAD_AXIS_DEFINITION_AXIS_Y: SolidLoadAxisDefinitionAxis
SOLID_LOAD_AXIS_DEFINITION_AXIS_Z: SolidLoadAxisDefinitionAxis
SOLID_LOAD_AXIS_DEFINITION_AXIS_ORIENTATION_POSITIVE: SolidLoadAxisDefinitionAxisOrientation
SOLID_LOAD_AXIS_DEFINITION_AXIS_ORIENTATION_NEGATIVE: SolidLoadAxisDefinitionAxisOrientation
SOLID_LOAD_GAS_BEHAVIOUR_RESULTING_OVERPRESSURE: SolidLoadGasBehaviour
SOLID_LOAD_GAS_BEHAVIOUR_OVERPRESSURE_INCREMENT: SolidLoadGasBehaviour
SOLID_LOAD_GAS_BEHAVIOUR_RESULTING_VOLUME: SolidLoadGasBehaviour
SOLID_LOAD_GAS_BEHAVIOUR_VOLUME_INCREMENT: SolidLoadGasBehaviour

class SolidLoad(_message.Message):
    __slots__ = ("no", "load_type", "solids", "load_case", "load_distribution", "load_direction", "load_direction_orientation", "uniform_magnitude", "magnitude_1", "magnitude_2", "strain_uniform_magnitude_x", "strain_uniform_magnitude_y", "strain_uniform_magnitude_z", "strain_magnitude_x1", "strain_magnitude_y1", "strain_magnitude_z1", "strain_magnitude_x2", "strain_magnitude_y2", "strain_magnitude_z2", "node_1", "node_2", "is_density_defined_by_altitude", "altitude", "angular_velocity", "angular_acceleration", "axis_definition_type", "axis_definition_p1", "axis_definition_p1_x", "axis_definition_p1_y", "axis_definition_p1_z", "axis_definition_p2", "axis_definition_p2_x", "axis_definition_p2_y", "axis_definition_p2_z", "axis_definition_axis", "axis_definition_axis_orientation", "gas_magnitude", "gas_behaviour", "coordinate_system", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    LOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOLIDS_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    LOAD_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    UNIFORM_MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_2_FIELD_NUMBER: _ClassVar[int]
    STRAIN_UNIFORM_MAGNITUDE_X_FIELD_NUMBER: _ClassVar[int]
    STRAIN_UNIFORM_MAGNITUDE_Y_FIELD_NUMBER: _ClassVar[int]
    STRAIN_UNIFORM_MAGNITUDE_Z_FIELD_NUMBER: _ClassVar[int]
    STRAIN_MAGNITUDE_X1_FIELD_NUMBER: _ClassVar[int]
    STRAIN_MAGNITUDE_Y1_FIELD_NUMBER: _ClassVar[int]
    STRAIN_MAGNITUDE_Z1_FIELD_NUMBER: _ClassVar[int]
    STRAIN_MAGNITUDE_X2_FIELD_NUMBER: _ClassVar[int]
    STRAIN_MAGNITUDE_Y2_FIELD_NUMBER: _ClassVar[int]
    STRAIN_MAGNITUDE_Z2_FIELD_NUMBER: _ClassVar[int]
    NODE_1_FIELD_NUMBER: _ClassVar[int]
    NODE_2_FIELD_NUMBER: _ClassVar[int]
    IS_DENSITY_DEFINED_BY_ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_X_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_Y_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_Z_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_X_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_Y_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_Z_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_AXIS_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_AXIS_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    GAS_MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    GAS_BEHAVIOUR_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    load_type: SolidLoadLoadType
    solids: _containers.RepeatedScalarFieldContainer[int]
    load_case: int
    load_distribution: SolidLoadLoadDistribution
    load_direction: SolidLoadLoadDirection
    load_direction_orientation: SolidLoadLoadDirectionOrientation
    uniform_magnitude: float
    magnitude_1: float
    magnitude_2: float
    strain_uniform_magnitude_x: float
    strain_uniform_magnitude_y: float
    strain_uniform_magnitude_z: float
    strain_magnitude_x1: float
    strain_magnitude_y1: float
    strain_magnitude_z1: float
    strain_magnitude_x2: float
    strain_magnitude_y2: float
    strain_magnitude_z2: float
    node_1: int
    node_2: int
    is_density_defined_by_altitude: bool
    altitude: float
    angular_velocity: float
    angular_acceleration: float
    axis_definition_type: SolidLoadAxisDefinitionType
    axis_definition_p1: _common_pb2.Vector3d
    axis_definition_p1_x: float
    axis_definition_p1_y: float
    axis_definition_p1_z: float
    axis_definition_p2: _common_pb2.Vector3d
    axis_definition_p2_x: float
    axis_definition_p2_y: float
    axis_definition_p2_z: float
    axis_definition_axis: SolidLoadAxisDefinitionAxis
    axis_definition_axis_orientation: SolidLoadAxisDefinitionAxisOrientation
    gas_magnitude: float
    gas_behaviour: SolidLoadGasBehaviour
    coordinate_system: int
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., load_type: _Optional[_Union[SolidLoadLoadType, str]] = ..., solids: _Optional[_Iterable[int]] = ..., load_case: _Optional[int] = ..., load_distribution: _Optional[_Union[SolidLoadLoadDistribution, str]] = ..., load_direction: _Optional[_Union[SolidLoadLoadDirection, str]] = ..., load_direction_orientation: _Optional[_Union[SolidLoadLoadDirectionOrientation, str]] = ..., uniform_magnitude: _Optional[float] = ..., magnitude_1: _Optional[float] = ..., magnitude_2: _Optional[float] = ..., strain_uniform_magnitude_x: _Optional[float] = ..., strain_uniform_magnitude_y: _Optional[float] = ..., strain_uniform_magnitude_z: _Optional[float] = ..., strain_magnitude_x1: _Optional[float] = ..., strain_magnitude_y1: _Optional[float] = ..., strain_magnitude_z1: _Optional[float] = ..., strain_magnitude_x2: _Optional[float] = ..., strain_magnitude_y2: _Optional[float] = ..., strain_magnitude_z2: _Optional[float] = ..., node_1: _Optional[int] = ..., node_2: _Optional[int] = ..., is_density_defined_by_altitude: bool = ..., altitude: _Optional[float] = ..., angular_velocity: _Optional[float] = ..., angular_acceleration: _Optional[float] = ..., axis_definition_type: _Optional[_Union[SolidLoadAxisDefinitionType, str]] = ..., axis_definition_p1: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., axis_definition_p1_x: _Optional[float] = ..., axis_definition_p1_y: _Optional[float] = ..., axis_definition_p1_z: _Optional[float] = ..., axis_definition_p2: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., axis_definition_p2_x: _Optional[float] = ..., axis_definition_p2_y: _Optional[float] = ..., axis_definition_p2_z: _Optional[float] = ..., axis_definition_axis: _Optional[_Union[SolidLoadAxisDefinitionAxis, str]] = ..., axis_definition_axis_orientation: _Optional[_Union[SolidLoadAxisDefinitionAxisOrientation, str]] = ..., gas_magnitude: _Optional[float] = ..., gas_behaviour: _Optional[_Union[SolidLoadGasBehaviour, str]] = ..., coordinate_system: _Optional[int] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
