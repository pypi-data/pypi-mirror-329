from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ResultsId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESULTS_ID_INVALID: _ClassVar[ResultsId]
    RESULTS_ID_STATIC_ANALYSIS_MEMBER_INTERNAL_FORCES: _ClassVar[ResultsId]
    RESULTS_ID_TEST: _ClassVar[ResultsId]
RESULTS_ID_INVALID: ResultsId
RESULTS_ID_STATIC_ANALYSIS_MEMBER_INTERNAL_FORCES: ResultsId
RESULTS_ID_TEST: ResultsId
