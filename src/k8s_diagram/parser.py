import pprint
from dataclasses import dataclass
from typing import Self

from kubernetes.client import ApiClient, AppsV1Api, BatchV1Api, CoreV1Api, CustomObjectsApi

from k8s_diagram.types.kubernetes import App, CronJob, Deployment, Job, Namespace, Pod, ReplicaSet, Service, StatefulSet


@dataclass
class Parser:
    api_client: ApiClient
    namespaces: dict[str, Namespace] | None = None
    services: dict[str, Service] | None = None
    pods: dict[str, Pod] | None = None
    deployments: dict[str, Deployment] | None = None
    replica_sets: dict[str, ReplicaSet] | None = None
    stateful_sets: dict[str, StatefulSet] | None = None
    jobs: dict[str, Job] | None = None
    cron_jobs: dict[str, CronJob] | None = None
    apps: list[App] | None = None

    @property
    def core_v1_api(self) -> CoreV1Api:
        return CoreV1Api(api_client=self.api_client)

    @property
    def apps_v1_api(self) -> AppsV1Api:
        return AppsV1Api(api_client=self.api_client)

    @property
    def custom_object_api(self) -> CustomObjectsApi:
        return CustomObjectsApi(api_client=self.api_client)

    @property
    def batch_v1_api(self) -> BatchV1Api:
        return BatchV1Api(api_client=self.api_client)

    def parse(self) -> None:
        (
            self.parse_namespaces()
                .parse_services()
                .parse_pods()
                .parse_deployments()
                .parse_replica_sets()
                .parse_stateful_sets()
                .parse_jobs()
                .parse_cron_jobs()
                .associate_services_with_namespaces()
                .associate_pods_with_namespaces()
                .associate_pods_with_services()
                .associate_deployments_with_namespaces()
                .associate_replica_sets_with_namespaces()
                .associate_replica_sets_with_deployments()
                .associate_pods_with_replica_sets()
                .associate_stateful_sets_with_namespaces()
                .associate_pods_with_stateful_sets()
                .associate_jobs_with_namespaces()
                .associate_pods_with_jobs()
                .associate_cron_jobs_with_namespaces()
                .associate_jobs_with_cron_jobs()
        )

    def parse_namespaces(self) -> Self:
        self.namespaces = dict()

        for v1_namespace in self.core_v1_api.list_namespace().items:
            namespace = Namespace.from_object(v1_namespace)

            self.namespaces[namespace.name] = namespace

        return self

    def parse_services(self) -> Self:
        self.services = dict()

        for v1_service in self.core_v1_api.list_service_for_all_namespaces().items:
            service = Service.from_object(v1_service)

            self.services[service.name] = service

        return self

    def parse_pods(self) -> Self:
        self.pods = dict()

        for v1_pod in self.core_v1_api.list_pod_for_all_namespaces().items:
            pod = Pod.from_object(v1_pod)

            self.pods[pod.uid] = pod

        return self

    def parse_deployments(self) -> Self:
        self.deployments = dict()

        for v1_deployment in self.apps_v1_api.list_deployment_for_all_namespaces().items:
            deployment = Deployment.from_object(v1_deployment)

            self.deployments[deployment.name] = deployment

        return self

    def parse_replica_sets(self) -> Self:
        self.replica_sets = dict()

        for v1_replica_set in self.apps_v1_api.list_replica_set_for_all_namespaces().items:
            replica_set = ReplicaSet.from_object(v1_replica_set)

            self.replica_sets[replica_set.name] = replica_set

        return self

    def parse_stateful_sets(self) -> Self:
        self.stateful_sets = dict()

        for v1_stateful_set in self.apps_v1_api.list_stateful_set_for_all_namespaces().items:
            stateful_set = StatefulSet.from_object(v1_stateful_set)
            self.stateful_sets[stateful_set.name] = stateful_set

        return self

    def parse_jobs(self) -> Self:
        self.jobs = dict()

        for v1_job in self.batch_v1_api.list_job_for_all_namespaces().items:
            job = Job.from_object(v1_job)
            self.jobs[job.name] = job

        return self

    def parse_cron_jobs(self) -> Self:
        self.cron_jobs = dict()

        for v1_cron_job in self.batch_v1_api.list_cron_job_for_all_namespaces().items:
            cron_job = CronJob.from_object(v1_cron_job)
            self.cron_jobs[cron_job.name] = cron_job

        return self

    def associate_services_with_namespaces(self) -> Self:
        for service in self.services.values():
            namespace = self.namespaces[service.namespace]
            namespace.add_service(service)

        return self

    def associate_pods_with_namespaces(self) -> Self:
        for pod in self.pods.values():
            namespace = self.namespaces[pod.namespace]
            namespace.add_pod(pod)

        return self

    def associate_pods_with_services(self) -> Self:
        for service in self.services.values():
            if service.selectors is not None:
                for pod in self.pods.values():
                    has_labels = True
                    for key, value in service.selectors.items():
                        has_labels = has_labels and (key in pod.labels and pod.labels[key] == value)

                    if has_labels:
                        service.add_pod(pod)

        return self

    def associate_deployments_with_namespaces(self) -> Self:
        for deployment in self.deployments.values():
            namespace = self.namespaces[deployment.namespace]
            namespace.add_deployment(deployment)

        return self

    def associate_replica_sets_with_namespaces(self) -> Self:
        for replica_set in self.replica_sets.values():
            namespace = self.namespaces[replica_set.namespace]
            namespace.add_replica_set(replica_set)

        return self

    def associate_replica_sets_with_deployments(self) -> Self:
        for replica_set in self.replica_sets.values():
            deployment = self.deployments[replica_set.deployment_name]
            deployment.add_replica_set(replica_set)

        return self

    def associate_pods_with_replica_sets(self) -> Self:
        for pod in self.pods.values():
            if pod.replica_set_name in self.replica_sets:
                replica_set = self.replica_sets[pod.replica_set_name]
                replica_set.add_pod(pod)

        return self

    def associate_stateful_sets_with_namespaces(self) -> Self:
        for stateful_set in self.stateful_sets.values():
            namespace = self.namespaces[stateful_set.namespace]
            namespace.add_stateful_set(stateful_set)

        return self

    def associate_pods_with_stateful_sets(self) -> Self:
        for stateful_set in self.stateful_sets.values():
            if stateful_set.selectors is not None:
                for pod in self.pods.values():
                    has_labels = True
                    for key, value in stateful_set.selectors.items():
                        has_labels = has_labels and (key in pod.labels and pod.labels[key] == value)

                    if has_labels:
                        stateful_set.add_pod(pod)

        return self

    def associate_jobs_with_namespaces(self) -> Self:
        for job in self.jobs.values():
            namespace = self.namespaces[job.namespace]
            namespace.add_job(job)

        return self

    def associate_pods_with_jobs(self) -> Self:
        for pod in self.pods.values():
            if pod.job_name in self.jobs:
                job = self.jobs[pod.job_name]
                job.add_pod(pod)

        return self

    def associate_cron_jobs_with_namespaces(self) -> Self:
        for cron_job in self.cron_jobs.values():
            namespace = self.namespaces[cron_job.namespace]
            namespace.add_cron_job(cron_job)

        return self

    def associate_jobs_with_cron_jobs(self) -> Self:
        for job in self.jobs.values():
            if job.cron_job_name in self.cron_jobs:
                cron_job = self.cron_jobs[job.cron_job_name]
                cron_job.add_job(job)

        return self
