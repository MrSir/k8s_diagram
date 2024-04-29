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
        css_class: str | None = None
    ):
        super().__init__('pod_', name, uid, namespace=namespace, css_class=css_class)

        self.replica_set_name = replica_set_name
        self.job_name = job_name
        self.labels = labels

    @classmethod
    def from_object(cls, pod: V1Pod) -> Self:
        metadata: V1ObjectMeta = pod.metadata
        owner_references = metadata.owner_references

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
            uid=metadata.uid,
            namespace=metadata.namespace,
            labels=metadata.labels,
            replica_set_name=replica_set_name,
            job_name=job_name,
            css_class="pod"
        )


class Job(GraphNode):
    def __init__(self, name: str, uid: str, namespace: str, cron_job_name: str | None = None, css_class: str | None = None):
        super().__init__('job_', name, uid, namespace=namespace, css_class=css_class)

        self.cron_job_name = cron_job_name
        self.pods: list[Pod] = []

    @classmethod
    def from_object(cls, job: V1Job) -> Self:
        metadata: V1ObjectMeta = job.metadata
        owner_references = metadata.owner_references

        cron_job_name = None
        if owner_references is not None:
            cron_job_references = list(filter(lambda ref: ref.kind == 'CronJob', owner_references))
            if len(cron_job_references) == 1:
                cron_job_name = cron_job_references[0].name

        return cls(
            name=metadata.name,
            uid=metadata.uid,
            namespace=metadata.namespace,
            cron_job_name=cron_job_name,
            css_class="job",
        )

    def add_pod(self, pod: Pod) -> None:
        self.pods.append(pod)

    def relations_to_mermaid_js_code(self) -> str:
        if len(self.pods) == 0:
            return ""

        pod_ids = " & ".join([p.id for p in self.pods])

        return f"{self.id} --> {pod_ids}\n"


class CronJob(GraphNode):
    def __init__(self, name: str, uid: str, namespace: str, css_class: str | None = None):
        super().__init__('cjob_', name, uid, namespace=namespace, css_class=css_class)

        self.jobs: list[Job] = []

    @classmethod
    def from_object(cls, job: V1CronJob) -> Self:
        metadata: V1ObjectMeta = job.metadata

        return cls(
            name=metadata.name,
            uid=metadata.uid,
            namespace=metadata.namespace,
            css_class="cjob",
        )

    def add_job(self, job: Job) -> None:
        self.jobs.append(job)

    def relations_to_mermaid_js_code(self) -> str:
        if len(self.jobs) == 0:
            return ""

        job_ids = " & ".join([j.id for j in self.jobs])

        return f"{self.id} --> {job_ids}\n"


class StatefulSet(GraphNode):
    def __init__(self, name: str, uid: str, namespace: str, selectors: dict[str, str], css_class: str | None = None):
        super().__init__('sset_', name, uid, namespace=namespace, css_class=css_class)

        self.pods: list[Pod] = []
        self.selectors: dict[str, str] = selectors

    @classmethod
    def from_object(cls, stateful_set: V1StatefulSet) -> Self:
        metadata: V1ObjectMeta = stateful_set.metadata
        spec: V1StatefulSetSpec = stateful_set.spec
        selector: V1LabelSelector = spec.selector

        return cls(
            name=metadata.name,
            uid=metadata.uid,
            namespace=metadata.namespace,
            selectors=selector.match_labels,
            css_class="sset",
        )

    def add_pod(self, pod: Pod) -> None:
        self.pods.append(pod)

    def relations_to_mermaid_js_code(self) -> str:
        if len(self.pods) == 0:
            return ""

        pod_ids = " & ".join([p.id for p in self.pods])

        return f"{self.id} --> {pod_ids}\n"


class ReplicaSet(GraphNode):
    def __init__(
        self,
        name: str,
        uid: str,
        namespace: str,
        deployment_name: str,
        css_class: str | None = None
    ):
        super().__init__('rset_', name, uid, namespace=namespace, css_class=css_class)

        self.deployment_name: str = deployment_name
        self.pods: list[Pod] = []

    @classmethod
    def from_object(cls, replica_set: V1ReplicaSet) -> Self:
        metadata: V1ObjectMeta = replica_set.metadata
        owner_references = metadata.owner_references

        deployment_reference = list(filter(lambda ref: ref.kind == 'Deployment', owner_references))[0]

        return cls(
            name=metadata.name,
            uid=metadata.uid,
            namespace=metadata.namespace,
            deployment_name=deployment_reference.name,
            css_class="rset"
        )

    def add_pod(self, pod: Pod) -> None:
        self.pods.append(pod)

    def relations_to_mermaid_js_code(self) -> str:
        if len(self.pods) == 0:
            return ""

        pod_ids = " & ".join([p.id for p in self.pods])

        return f"{self.id} --> {pod_ids}\n"


class Deployment(GraphNode):
    def __init__(self, name: str, uid: str, namespace: str, css_class: str | None = None):
        super().__init__('dep_', name, uid, namespace=namespace, css_class=css_class)

        self.replica_sets: list[ReplicaSet] = []

    @classmethod
    def from_object(cls, deployment: V1Deployment) -> Self:
        metadata: V1ObjectMeta = deployment.metadata

        return cls(
            name=metadata.name,
            uid=metadata.uid,
            namespace=metadata.namespace,
            css_class="dep"
        )

    def add_replica_set(self, replica_set: ReplicaSet) -> None:
        self.replica_sets.append(replica_set)

    def relations_to_mermaid_js_code(self) -> str:
        relations = ""

        if len(self.replica_sets) > 0:
            replica_set_ids = " & ".join([rs.id for rs in self.replica_sets])
            relations += f"{self.id} --> {replica_set_ids}\n"

        return relations


class Service(GraphNode):
    def __init__(self, name: str, uid: str, namespace: str, selectors: dict[str, str], css_class: str | None = None):
        super().__init__('svc_', name, uid, namespace=namespace, css_class=css_class)

        self.pods: list[Pod] = []
        self.selectors: dict[str, str] = selectors

    @classmethod
    def from_object(cls, service: V1Service) -> Self:
        metadata: V1ObjectMeta = service.metadata
        spec: V1ServiceSpec = service.spec

        return cls(
            name=metadata.name,
            uid=metadata.uid,
            namespace=metadata.namespace,
            selectors=spec.selector,
            css_class="svc"
        )

    def add_pod(self, pod: Pod) -> None:
        self.pods.append(pod)

    def relations_to_mermaid_js_code(self) -> str:
        if len(self.pods) == 0:
            return ""

        pod_ids = " & ".join([p.id for p in self.pods])

        return f"{pod_ids} --> {self.id}\n"


class App(SubGraph):
    def __init__(self, name: str):
        super().__init__('App', name)


class Namespace(SubGraph):
    def __init__(self, name: str, uid: str, status_phase: str):
        super().__init__('Namespace', name, uid)

        self.status_phase = status_phase
        self.services: list[Service] = []
        self.pods: list[Pod] = []
        self.deployments: list[Deployment] = []
        self.replica_sets: list[ReplicaSet] = []
        self.stateful_sets: list[StatefulSet] = []
        self.jobs: list[Job] = []
        self.cron_jobs: list[CronJob] = []

    @classmethod
    def from_object(cls, namespace: V1Namespace) -> Self:
        metadata: V1ObjectMeta = namespace.metadata

        return cls(
            name=metadata.name,
            uid=metadata.uid,
            status_phase=namespace.status.phase
        )

    def to_mermaid_js_code(self) -> str:
        code = super().to_mermaid_js_code()

        for service in self.services:
            code += service.relations_to_mermaid_js_code()

        for deployment in self.deployments:
            code += deployment.relations_to_mermaid_js_code()

        for replica_set in self.replica_sets:
            code += replica_set.relations_to_mermaid_js_code()

        for stateful_set in self.stateful_sets:
            code += stateful_set.relations_to_mermaid_js_code()

        for job in self.jobs:
            code += job.relations_to_mermaid_js_code()

        for cron_job in self.cron_jobs:
            code += cron_job.relations_to_mermaid_js_code()

        return code

    def add_service(self, service: Service) -> None:
        self.services.append(service)

        if self.graph_nodes is None:
            self.graph_nodes = []

        self.graph_nodes.append(service)

    def add_pod(self, pod: Pod) -> None:
        self.pods.append(pod)

        if self.graph_nodes is None:
            self.graph_nodes = []

        self.graph_nodes.append(pod)

    def add_deployment(self, deployment: Deployment) -> None:
        self.deployments.append(deployment)

        if self.graph_nodes is None:
            self.graph_nodes = []

        self.graph_nodes.append(deployment)

    def add_replica_set(self, replica_set: ReplicaSet) -> None:
        self.replica_sets.append(replica_set)

        if self.graph_nodes is None:
            self.graph_nodes = []

        self.graph_nodes.append(replica_set)

    def add_stateful_set(self, stateful_set: StatefulSet) -> None:
        self.stateful_sets.append(stateful_set)

        if self.graph_nodes is None:
            self.graph_nodes = []

        self.graph_nodes.append(stateful_set)

    def add_job(self, job: Job) -> None:
        self.jobs.append(job)

        if self.graph_nodes is None:
            self.graph_nodes = []

        self.graph_nodes.append(job)

    def add_cron_job(self, cron_job: CronJob) -> None:
        self.cron_jobs.append(cron_job)

        if self.graph_nodes is None:
            self.graph_nodes = []

        self.graph_nodes.append(cron_job)
