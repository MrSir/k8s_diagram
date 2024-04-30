from typing import Self

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
        css_class: str | None = None
    ):
        super().__init__('pod_', name, uid, namespace=namespace, app=app, css_class=css_class)

        self.replica_set_name = replica_set_name
        self.job_name = job_name
        self.labels = labels

    @classmethod
    def from_object(cls, pod: V1Pod, uid: str) -> Self:
        metadata: V1ObjectMeta = pod.metadata
        owner_references = metadata.owner_references

        app = None
        if metadata.labels is not None and "app.kubernetes.io/name" in metadata.labels:
            app = metadata.labels["app.kubernetes.io/name"]
        elif metadata.labels is not None and "app" in metadata.labels:
            app = metadata.labels["app"]

        replica_set_name = None
        job_name = None
        if owner_references is not None and len(owner_references) > 0:
            replica_set_reference = list(filter(lambda ref: ref.kind == 'ReplicaSet', owner_references))
            if len(replica_set_reference) == 1:
                replica_set_name = replica_set_reference[0].name

            job_reference = list(filter(lambda ref: ref.kind == 'Job', owner_references))
            if len(job_reference) == 1:
                job_name = job_reference[0].name

        return cls(
            name=metadata.name,
            uid=uid,
            namespace=metadata.namespace,
            labels=metadata.labels,
            replica_set_name=replica_set_name,
            job_name=job_name,
            app=app,
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
        css_class: str | None = None
    ):
        super().__init__('job_', name, uid, namespace=namespace, app=name, css_class=css_class)

        self.cron_job_name = cron_job_name

    @classmethod
    def from_object(cls, job: V1Job, uid: str) -> Self:
        metadata: V1ObjectMeta = job.metadata
        owner_references = metadata.owner_references

        app = None
        if metadata.labels is not None and "app.kubernetes.io/name" in metadata.labels:
            app = metadata.labels["app.kubernetes.io/name"]
        elif metadata.labels is not None and "app" in metadata.labels:
            app = metadata.labels["app"]

        cron_job_name = None
        if owner_references is not None:
            cron_job_references = list(filter(lambda ref: ref.kind == 'CronJob', owner_references))
            if len(cron_job_references) == 1:
                cron_job_name = cron_job_references[0].name

        return cls(
            name=metadata.name,
            uid=uid,
            namespace=metadata.namespace,
            cron_job_name=cron_job_name,
            app=app,
            css_class="job",
        )


class CronJob(GraphNode):
    def __init__(self, name: str, uid: str, namespace: str, app: str | None = None, css_class: str | None = None):
        super().__init__('cjob_', name, uid, namespace=namespace, app=app, css_class=css_class)

    @classmethod
    def from_object(cls, job: V1CronJob, uid: str) -> Self:
        metadata: V1ObjectMeta = job.metadata

        app = None
        if metadata.labels is not None and "app.kubernetes.io/name" in metadata.labels:
            app = metadata.labels["app.kubernetes.io/name"]
        elif metadata.labels is not None and "app" in metadata.labels:
            app = metadata.labels["app"]

        return cls(
            name=metadata.name,
            uid=uid,
            namespace=metadata.namespace,
            app=app,
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
        css_class: str | None = None
    ):
        super().__init__('sset_', name, uid, namespace=namespace, app=app, css_class=css_class)

        self.selectors: dict[str, str] = selectors

    @classmethod
    def from_object(cls, stateful_set: V1StatefulSet, uid: str) -> Self:
        metadata: V1ObjectMeta = stateful_set.metadata
        spec: V1StatefulSetSpec = stateful_set.spec
        selector: V1LabelSelector = spec.selector

        app = None
        if metadata.labels is not None and "app.kubernetes.io/name" in metadata.labels:
            app = metadata.labels["app.kubernetes.io/name"]
        elif metadata.labels is not None and "app" in metadata.labels:
            app = metadata.labels["app"]

        return cls(
            name=metadata.name,
            uid=uid,
            namespace=metadata.namespace,
            selectors=selector.match_labels,
            app=app,
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
        css_class: str | None = None
    ):
        super().__init__('rset_', name, uid, namespace=namespace, app=app, css_class=css_class)

        self.deployment_name: str = deployment_name

    @classmethod
    def from_object(cls, replica_set: V1ReplicaSet, uid: str) -> Self:
        metadata: V1ObjectMeta = replica_set.metadata
        owner_references = metadata.owner_references

        deployment_reference = list(filter(lambda ref: ref.kind == 'Deployment', owner_references))[0]

        app = None
        if metadata.labels is not None and "app.kubernetes.io/name" in metadata.labels:
            app = metadata.labels["app.kubernetes.io/name"]
        elif metadata.labels is not None and "app" in metadata.labels:
            app = metadata.labels["app"]

        return cls(
            name=metadata.name,
            uid=uid,
            namespace=metadata.namespace,
            deployment_name=deployment_reference.name,
            app=app,
            css_class="rset"
        )


class Deployment(GraphNode):
    def __init__(
        self,
        name: str,
        uid: str,
        namespace: str,
        app: str | None = None,
        css_class: str | None = None
    ):
        super().__init__('dep_', name, uid, namespace=namespace, app=app, css_class=css_class)

    @classmethod
    def from_object(cls, deployment: V1Deployment, uid: str) -> Self:
        metadata: V1ObjectMeta = deployment.metadata

        app = None
        if metadata.labels is not None and "app.kubernetes.io/name" in metadata.labels:
            app = metadata.labels["app.kubernetes.io/name"]
        elif metadata.labels is not None and "app" in metadata.labels:
            app = metadata.labels["app"]

        return cls(
            name=metadata.name,
            uid=uid,
            namespace=metadata.namespace,
            app=app,
            css_class="dep"
        )


class Service(GraphNode):
    def __init__(
        self,
        name: str,
        uid: str,
        namespace: str,
        selectors: dict[str, str],
        app: str | None = None,
        css_class: str | None = None
    ):
        super().__init__('svc_', name, uid, namespace=namespace, app=app, css_class=css_class)

        self.selectors: dict[str, str] = selectors

    @classmethod
    def from_object(cls, service: V1Service, uid: str) -> Self:
        metadata: V1ObjectMeta = service.metadata

        app = None
        if metadata.labels is not None and "app.kubernetes.io/name" in metadata.labels:
            app = metadata.labels["app.kubernetes.io/name"]
        elif metadata.labels is not None and "app" in metadata.labels:
            app = metadata.labels["app"]

        spec: V1ServiceSpec = service.spec

        return cls(
            name=metadata.name,
            uid=uid,
            namespace=metadata.namespace,
            app=app,
            selectors=spec.selector,
            css_class="svc"
        )

    def relations_to_mermaid_js_code(self) -> str:
        if self.related_nodes is None or len(self.related_nodes) == 0:
            return ""

        related_node_ids = " & ".join([key for key in self.related_nodes.keys()])

        return f"{related_node_ids} --> {self.id}\n"


class App(SubGraph):
    def __init__(self, name: str, uid: str):
        super().__init__('App', name, uid)

    def to_mermaid_js_code(self) -> str:
        code = super().to_mermaid_js_code()

        for graph_node in self.graph_nodes.values():
            code += graph_node.relations_to_mermaid_js_code()

        return code


class Namespace(SubGraph):
    def __init__(self, name: str, uid: str, status_phase: str):
        super().__init__('Namespace', name, uid)

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

