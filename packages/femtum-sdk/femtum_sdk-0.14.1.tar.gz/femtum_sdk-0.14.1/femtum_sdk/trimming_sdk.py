import grpc
from femtum_sdk.core.wafer_pb2_grpc import WaferServiceStub
from femtum_sdk.core.reticle_pb2_grpc import ReticleServiceStub
from femtum_sdk.core.die_pb2_grpc import DieServiceStub
from femtum_sdk.core.circuit_pb2_grpc import CircuitServiceStub
from femtum_sdk.core.sweep_pb2_grpc import SweepServiceStub
from femtum_sdk.core.result_pb2_grpc import ResultServiceStub


class TrimmingSdk:
    def __init__(self, grpc_channel: grpc.Channel):
        self.grpc_channel = grpc_channel

    @property
    def wafer(self):
        return WaferServiceStub(self.grpc_channel)

    @property
    def reticle(self):
        return ReticleServiceStub(self.grpc_channel)

    @property
    def die(self):
        return DieServiceStub(self.grpc_channel)

    @property
    def circuit(self):
        return CircuitServiceStub(self.grpc_channel)

    @property
    def result(self):
        return ResultServiceStub(self.grpc_channel)

    @property
    def sweep(self):
        return SweepServiceStub(self.grpc_channel)
