from kubernetes.client import ApiClient, Configuration

from k8s_diagram.parser import Parser
from k8s_diagram.renderer import DiagramsRenderer, MermaidJSRenderer, RendererProtocol
from k8s_diagram.types.base import Graph


class FORMATS:
    MERMAID_JS = "mermaid-js"
    DIAGRAMS = "diagrams"


class K8sDiagrammer:
    def __init__(
        self,
        diagram_format: str,
        end_point: str,
        api_key: str,
        cert_path: str | None = None,
        included_namespaces: set[str] = None,
        excluded_namespaces: set[str] = None
    ):
        self.diagram_format = diagram_format
        self.end_point = end_point
        self.api_key = api_key
        self.cert_path = cert_path
        self.included_namespaces = included_namespaces
        self.excluded_namespaces = excluded_namespaces

    def api_client(self) -> ApiClient:
        configuration = Configuration(
            host=self.end_point,
            api_key={"authorization": self.api_key},
            api_key_prefix={"authorization": "Bearer"},
        )

        if self.cert_path is not None:
            configuration.ssl_ca_cert = self.cert_path

        return ApiClient(configuration=configuration)

    def parser(self) -> Parser:
        return Parser(api_client=self.api_client())

    def graph(self) -> Graph:
        return self.parser().parse(included_namespaces=self.included_namespaces, excluded_namespaces=self.excluded_namespaces)

    def renderer(self) -> RendererProtocol:
        match self.diagram_format:
            case FORMATS.MERMAID_JS:
                return MermaidJSRenderer(self.graph())
            case FORMATS.DIAGRAMS:
                return DiagramsRenderer(self.graph())

    def render(self) -> None:
        self.renderer().render()

