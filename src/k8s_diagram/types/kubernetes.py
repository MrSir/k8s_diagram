from typing import Self

from diagrams import Cluster
from diagrams.k8s.network import SVC
from diagrams.k8s.compute import Deploy, Pod as P, RS, Job as J, Cronjob as CJ, STS
from kubernetes.client import (
    V1CronJob, V1Job, V1JobSpec, V1LabelSelector,
    V1ObjectMeta,
    V1Namespace,
    V1Service,
    V1Pod,
    V1Deployment,
    V1ServiceSpec,
    V1StatefulSet,
    V1ReplicaSet,
    V1StatefulSetSpec,
)

from k8s_diagram.types.base import SubGraph, GraphNode


class Pod(GraphNode):
    def __init__(
        self,
        name: str,
        uid: str,
        namespace: str,
        labels: dict[str, str],
        replica_set_name: str | None = None,
        job_name: str | None = None,
        app: str | None = None,
        system: str | None = None,
        css_class: str | None = None
    ):
        super().__init__('pod_', name, uid, namespace=namespace, app=app, system=system, css_class=css_class)

        self.replica_set_name = replica_set_name
        self.job_name = job_name
        self.labels = labels
        self._diagrams_node: P | None = None

    @property
    def diagrams_node(self):
        if self._diagrams_node is None:
            self._diagrams_node = P(self.name)

        return self._diagrams_node

    @classmethod
    def from_object(cls, pod: V1Pod, uid: str) -> Self:
        metadata: V1ObjectMeta = pod.metadata
        owner_references = metadata.owner_references

        name = metadata.name

        replica_set_name = None
        job_name = None
        if owner_references is not None and len(owner_references) > 0:
            name = metadata.name.split("-")[-1]
            replica_set_reference = list(filter(lambda ref: ref.kind == 'ReplicaSet', owner_references))
            if len(replica_set_reference) == 1:
                replica_set_name = replica_set_reference[0].name.split("-")[-1]

            job_reference = list(filter(lambda ref: ref.kind == 'Job', owner_references))
            if len(job_reference) == 1:
                job_name = job_reference[0].name.split("-")[-1]

        return cls(
            name=name,
            uid=uid,
            namespace=metadata.namespace,
            labels=metadata.labels,
            replica_set_name=replica_set_name,
            job_name=job_name,
            app=cls.resolve_app_name(metadata),
            system=cls.resolve_system_name(metadata),
            css_class="pod"
        )


class Job(GraphNode):
    def __init__(
        self,
        name: str,
        uid: str,
        namespace: str,
        cron_job_name: str | None = None,
        app: str | None = None,
        system: str | None = None,
        css_class: str | None = None
    ):
        super().__init__('job_', name, uid, namespace=namespace, app=app, system=system, css_class=css_class)

        self.cron_job_name = cron_job_name
        self._diagrams_node: J | None = None

    @property
    def diagrams_node(self):
        if self._diagrams_node is None:
            self._diagrams_node = J(self.name)

        return self._diagrams_node

    @classmethod
    def from_object(cls, job: V1Job, uid: str) -> Self:
        metadata: V1ObjectMeta = job.metadata
        owner_references = metadata.owner_references

        name = metadata.name.split("-")[-1]

        cron_job_name = None
        if owner_references is not None:
            cron_job_references = list(filter(lambda ref: ref.kind == 'CronJob', owner_references))
            if len(cron_job_references) == 1:
                cron_job_name = cron_job_references[0].name

        return cls(
            name=name,
            uid=uid,
            namespace=metadata.namespace,
            cron_job_name=cron_job_name,
            app=cls.resolve_app_name(metadata),
            system=cls.resolve_system_name(metadata),
            css_class="job",
        )


class CronJob(GraphNode):
    def __init__(
        self,
        name: str,
        uid: str,
        namespace: str,
        app: str | None = None,
        system: str | None = None,
        css_class: str | None = None
    ):
        super().__init__('cjob_', name, uid, namespace=namespace, app=app, system=system, css_class=css_class)

        self._diagrams_node: CJ | None = None

    @property
    def diagrams_node(self):
        if self._diagrams_node is None:
            self._diagrams_node = CJ(self.name)

        return self._diagrams_node

    @classmethod
    def from_object(cls, job: V1CronJob, uid: str) -> Self:
        metadata: V1ObjectMeta = job.metadata

        return cls(
            name=metadata.name,
            uid=uid,
            namespace=metadata.namespace,
            app=cls.resolve_app_name(metadata),
            system=cls.resolve_system_name(metadata),
            css_class="cjob",
        )


class StatefulSet(GraphNode):
    def __init__(
        self,
        name: str,
        uid: str,
        namespace: str,
        selectors: dict[str, str],
        app: str | None = None,
        system: str | None = None,
        css_class: str | None = None
    ):
        super().__init__('sset_', name, uid, namespace=namespace, app=app, system=system, css_class=css_class)

        self.selectors: dict[str, str] = selectors

        self._diagrams_node: STS | None = None

    @property
    def diagrams_node(self):
        if self._diagrams_node is None:
            self._diagrams_node = STS(self.name)

        return self._diagrams_node
    @classmethod
    def from_object(cls, stateful_set: V1StatefulSet, uid: str) -> Self:
        metadata: V1ObjectMeta = stateful_set.metadata
        spec: V1StatefulSetSpec = stateful_set.spec
        selector: V1LabelSelector = spec.selector

        return cls(
            name=metadata.name,
            uid=uid,
            namespace=metadata.namespace,
            selectors=selector.match_labels,
            app=cls.resolve_app_name(metadata),
            system=cls.resolve_system_name(metadata),
            css_class="sset",
        )


class ReplicaSet(GraphNode):
    def __init__(
        self,
        name: str,
        uid: str,
        namespace: str,
        deployment_name: str,
        app: str | None = None,
        system: str | None = None,
        css_class: str | None = None
    ):
        super().__init__('rset_', name, uid, namespace=namespace, app=app, system=system, css_class=css_class)

        self.deployment_name: str = deployment_name
        self._diagrams_node: RS | None = None

    @classmethod
    def from_object(cls, replica_set: V1ReplicaSet, uid: str) -> Self:
        metadata: V1ObjectMeta = replica_set.metadata
        owner_references = metadata.owner_references

        name = metadata.name.split("-")[-1]

        deployment_reference = list(filter(lambda ref: ref.kind == 'Deployment', owner_references))[0]

        return cls(
            name=name,
            uid=uid,
            namespace=metadata.namespace,
            deployment_name=deployment_reference.name,
            app=cls.resolve_app_name(metadata),
            system=cls.resolve_system_name(metadata),
            css_class="rset"
        )

    @property
    def diagrams_node(self):
        if self._diagrams_node is None:
            self._diagrams_node = RS(self.name)

        return self._diagrams_node


class Deployment(GraphNode):
    def __init__(
        self,
        name: str,
        uid: str,
        namespace: str,
        app: str | None = None,
        system: str | None = None,
        css_class: str | None = None
    ):
        super().__init__('dep_', name, uid, namespace=namespace, app=app, system=system, css_class=css_class)

        self._diagrams_node: Deploy | None = None

    @classmethod
    def from_object(cls, deployment: V1Deployment, uid: str) -> Self:
        metadata: V1ObjectMeta = deployment.metadata

        return cls(
            name=metadata.name,
            uid=uid,
            namespace=metadata.namespace,
            app=cls.resolve_app_name(metadata),
            system=cls.resolve_system_name(metadata),
            css_class="dep"
        )

    @property
    def diagrams_node(self):
        if self._diagrams_node is None:
            self._diagrams_node = Deploy(self.name)

        return self._diagrams_node


class Service(GraphNode):
    def __init__(
        self,
        name: str,
        uid: str,
        namespace: str,
        selectors: dict[str, str],
        app: str | None = None,
        system: str | None = None,
        css_class: str | None = None
    ):
        super().__init__('svc_', name, uid, namespace=namespace, app=app, system=system, css_class=css_class)

        self.selectors: dict[str, str] = selectors
        self._diagrams_node: SVC | None = None

    @classmethod
    def from_object(cls, service: V1Service, uid: str) -> Self:
        metadata: V1ObjectMeta = service.metadata

        spec: V1ServiceSpec = service.spec

        return cls(
            name=metadata.name,
            uid=uid,
            namespace=metadata.namespace,
            app=cls.resolve_app_name(metadata),
            system=cls.resolve_system_name(metadata),
            selectors=spec.selector,
            css_class="svc"
        )

    def relations_to_mermaid_js_code(self) -> str:
        if self.related_nodes is None or len(self.related_nodes) == 0:
            return ""

        related_node_ids = " & ".join([key for key in self.related_nodes.keys()])

        return f"{related_node_ids} --> {self.id}\n"

    @property
    def diagrams_node(self):
        if self._diagrams_node is None:
            self._diagrams_node = SVC(self.name)

        return self._diagrams_node

    def to_diagrams(self) -> None:
        if self.related_nodes is not None:
            for node in self.related_nodes.values():
                node.diagrams_node >> self.diagrams_node


class App(SubGraph):
    def __init__(self, name: str, uid: str):
        super().__init__('App', name, uid)

        self.color = "#EBF3E7"

    def to_mermaid_js_code(self) -> str:
        code = super().to_mermaid_js_code()

        for graph_node in self.graph_nodes.values():
            code += graph_node.relations_to_mermaid_js_code()

        return code


class System(SubGraph):
    def __init__(self, name: str, uid: str):
        super().__init__('System', name, uid)

        self.color = "#E5F5FD"

    def to_mermaid_js_code(self) -> str:
        code = super().to_mermaid_js_code()

        for graph_node in self.graph_nodes.values():
            code += graph_node.relations_to_mermaid_js_code()

        return code


class Namespace(SubGraph):
    def __init__(self, name: str, uid: str, status_phase: str):
        super().__init__('Namespace', name, uid)

        self.color = "#f3e7f0"
        self.status_phase = status_phase
        self.graph_nodes = dict()

    @classmethod
    def from_object(cls, namespace: V1Namespace, uid: str) -> Self:
        metadata: V1ObjectMeta = namespace.metadata

        return cls(
            name=metadata.name,
            uid=uid,
            status_phase=namespace.status.phase
        )

    def to_mermaid_js_code(self) -> str:
        code = super().to_mermaid_js_code()

        for graph_node in self.graph_nodes.values():
            code += graph_node.relations_to_mermaid_js_code()

        return code
