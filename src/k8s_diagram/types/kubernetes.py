from typing import Self

from kubernetes.client import (
    V1ObjectMeta,
    V1Namespace,
    V1Service,
    V1Pod,
    V1Deployment,
    V1StatefulSet,
    V1DaemonSet,
    V1ReplicaSet
)

from k8s_diagram.types.base import SubGraph, GraphNode


class ReplicaSet(GraphNode):
    def __init__(self, name: str):
        super().__init__('rset_', name)

    @classmethod
    def from_object(cls, replica_set: V1ReplicaSet) -> Self:
        metadata: V1ObjectMeta = replica_set.metadata

        return cls(name=metadata.name)


class DaemonSet(GraphNode):
    def __init__(self, name: str):
        super().__init__('dset_', name)

    @classmethod
    def from_object(cls, daemon_set: V1DaemonSet) -> Self:
        metadata: V1ObjectMeta = daemon_set.metadata

        return cls(name=metadata.name)


class StatefulSet(GraphNode):
    def __init__(self, name: str):
        super().__init__('sset_', name)

    @classmethod
    def from_object(cls, stateful_set: V1StatefulSet) -> Self:
        metadata: V1ObjectMeta = stateful_set.metadata

        return cls(name=metadata.name)


class Deployment(GraphNode):
    def __init__(self, name: str):
        super().__init__('dep_', name)

    @classmethod
    def from_object(cls, deployment: V1Deployment) -> Self:
        metadata: V1ObjectMeta = deployment.metadata

        return cls(name=metadata.name)


class Pod(GraphNode):
    def __init__(self, name: str):
        super().__init__('pod_', name)

    @classmethod
    def from_object(cls, pod: V1Pod) -> Self:
        metadata: V1ObjectMeta = pod.metadata

        return cls(name=metadata.name)


class Service(GraphNode):
    def __init__(self, name: str):
        super().__init__('svc_', name)

    @classmethod
    def from_object(cls, service: V1Service) -> Self:
        metadata: V1ObjectMeta = service.metadata

        return cls(name=metadata.name)


class App(SubGraph):
    def __init__(self, name: str):
        super().__init__('App', name)


class Namespace(SubGraph):
    def __init__(self, name: str):
        super().__init__('Namespace', name)

    @classmethod
    def from_object(cls, namespace: V1Namespace) -> Self:
        metadata: V1ObjectMeta = namespace.metadata

        return cls(name=metadata.name)
