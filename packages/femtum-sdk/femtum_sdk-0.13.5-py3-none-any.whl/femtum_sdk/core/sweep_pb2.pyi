import femtum_sdk.core.tag_pb2 as _tag_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SweepRequest(_message.Message):
    __slots__ = ("WaferName", "ReticleName", "DieName", "CircuitName", "ResultName", "Tags", "SweepInput")
    WAFERNAME_FIELD_NUMBER: _ClassVar[int]
    RETICLENAME_FIELD_NUMBER: _ClassVar[int]
    DIENAME_FIELD_NUMBER: _ClassVar[int]
    CIRCUITNAME_FIELD_NUMBER: _ClassVar[int]
    RESULTNAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    SWEEPINPUT_FIELD_NUMBER: _ClassVar[int]
    WaferName: str
    ReticleName: str
    DieName: str
    CircuitName: str
    ResultName: str
    Tags: _containers.RepeatedCompositeFieldContainer[_tag_pb2.Tag]
    SweepInput: SweepInput
    def __init__(self, WaferName: _Optional[str] = ..., ReticleName: _Optional[str] = ..., DieName: _Optional[str] = ..., CircuitName: _Optional[str] = ..., ResultName: _Optional[str] = ..., Tags: _Optional[_Iterable[_Union[_tag_pb2.Tag, _Mapping]]] = ..., SweepInput: _Optional[_Union[SweepInput, _Mapping]] = ...) -> None: ...

class SweepOutput(_message.Message):
    __slots__ = ("Id", "WavelengthsArray", "PowersArray", "Tags")
    ID_FIELD_NUMBER: _ClassVar[int]
    WAVELENGTHSARRAY_FIELD_NUMBER: _ClassVar[int]
    POWERSARRAY_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    Id: str
    WavelengthsArray: _containers.RepeatedScalarFieldContainer[float]
    PowersArray: _containers.RepeatedScalarFieldContainer[float]
    Tags: _containers.RepeatedCompositeFieldContainer[_tag_pb2.Tag]
    def __init__(self, Id: _Optional[str] = ..., WavelengthsArray: _Optional[_Iterable[float]] = ..., PowersArray: _Optional[_Iterable[float]] = ..., Tags: _Optional[_Iterable[_Union[_tag_pb2.Tag, _Mapping]]] = ...) -> None: ...

class SweepInput(_message.Message):
    __slots__ = ("WavelengthStart_nm", "WavelengthStop_nm", "Sampling_pm", "LaserSpeed_nm_per_s", "LaserPower_dbm")
    WAVELENGTHSTART_NM_FIELD_NUMBER: _ClassVar[int]
    WAVELENGTHSTOP_NM_FIELD_NUMBER: _ClassVar[int]
    SAMPLING_PM_FIELD_NUMBER: _ClassVar[int]
    LASERSPEED_NM_PER_S_FIELD_NUMBER: _ClassVar[int]
    LASERPOWER_DBM_FIELD_NUMBER: _ClassVar[int]
    WavelengthStart_nm: float
    WavelengthStop_nm: float
    Sampling_pm: int
    LaserSpeed_nm_per_s: int
    LaserPower_dbm: float
    def __init__(self, WavelengthStart_nm: _Optional[float] = ..., WavelengthStop_nm: _Optional[float] = ..., Sampling_pm: _Optional[int] = ..., LaserSpeed_nm_per_s: _Optional[int] = ..., LaserPower_dbm: _Optional[float] = ...) -> None: ...

class StoreSweepRequest(_message.Message):
    __slots__ = ("Sweep", "Data")
    SWEEP_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    Sweep: SweepRequest
    Data: SpectrumData
    def __init__(self, Sweep: _Optional[_Union[SweepRequest, _Mapping]] = ..., Data: _Optional[_Union[SpectrumData, _Mapping]] = ...) -> None: ...

class StoreSweepAfterShotRequest(_message.Message):
    __slots__ = ("Sweep", "Data", "ShotNumber")
    SWEEP_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SHOTNUMBER_FIELD_NUMBER: _ClassVar[int]
    Sweep: SweepRequest
    Data: SpectrumData
    ShotNumber: int
    def __init__(self, Sweep: _Optional[_Union[SweepRequest, _Mapping]] = ..., Data: _Optional[_Union[SpectrumData, _Mapping]] = ..., ShotNumber: _Optional[int] = ...) -> None: ...

class SpectrumData(_message.Message):
    __slots__ = ("WavelengthsArray", "PowersArray")
    WAVELENGTHSARRAY_FIELD_NUMBER: _ClassVar[int]
    POWERSARRAY_FIELD_NUMBER: _ClassVar[int]
    WavelengthsArray: _containers.RepeatedScalarFieldContainer[float]
    PowersArray: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, WavelengthsArray: _Optional[_Iterable[float]] = ..., PowersArray: _Optional[_Iterable[float]] = ...) -> None: ...
