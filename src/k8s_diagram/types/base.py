import uuid
from abc import abstractmethod
from dataclasses import dataclass

from diagrams import Cluster, Diagram
from kubernetes.client import V1ObjectMeta


@dataclass
class GraphNode:
    prefix: str
    name: str
    uid: str
    namespace: str | None = None
    app: str | None = None
    system: str | None = None
    css_class: str | None = None
    related_nodes: dict[str, "GraphNode"] | None = None
    __id: str | None = None

    @property
    def id(self) -> str:
        if self.__id is None:
            self.__id = f"{self.prefix}{self.uid}"

        return self.__id

    def add_related_node(self, graph_node: "GraphNode") -> None:
        if self.related_nodes is None:
            self.related_nodes = dict()

        self.related_nodes[graph_node.id] = graph_node

    def to_mermaid_js_code(self) -> str:
        style = ""
        if self.css_class is not None:
            style += f":::{self.css_class}"

        return f"{self.id}(\"{self.name}\"){style}\n"

    def relations_to_mermaid_js_code(self) -> str:
        if self.related_nodes is None or len(self.related_nodes) == 0:
            return ""

        related_node_ids = " & ".join([key for key in self.related_nodes.keys()])

        return f"{self.id} --> {related_node_ids}\n"

    def to_diagrams(self) -> None:
        diagrams_node = self.diagrams_node

        if self.related_nodes is not None:
            for node in self.related_nodes.values():
                diagrams_node >> node.diagrams_node

    @staticmethod
    def resolve_app_name(metadata: V1ObjectMeta) -> str | None:
        app = None
        if metadata.labels is not None:
            if "app.kubernetes.io/name" in metadata.labels:
                app = metadata.labels["app.kubernetes.io/name"]
            elif "app" in metadata.labels:
                app = metadata.labels["app"]

        return app

    @staticmethod
    def resolve_system_name(metadata: V1ObjectMeta) -> str | None:
        system = None
        if metadata.labels is not None and "app.kubernetes.io/part-of" in metadata.labels:
            system = metadata.labels["app.kubernetes.io/part-of"]

        return system


@dataclass
class Graph:
    title: str
    graph_nodes: dict[str, GraphNode] | None = None
    color: str | None = None

    @property
    def styles(self) -> str:
        style = f"classDef svc fill:red;\n"
        style += f"classDef pod fill:blue;\n"
        style += f"classDef dep fill:green;\n"
        style += f"classDef rset fill:yellow;\n"
        style += f"classDef sset fill:magenta;\n"
        style += f"classDef job fill:purple;\n"

        return style

    def add_graph_node(self, graph_node: GraphNode) -> None:
        if self.graph_nodes is None:
            self.graph_nodes = dict()

        self.graph_nodes[graph_node.id] = graph_node

    def add_graph_nodes(self, graph_nodes: dict[str, GraphNode]) -> None:
        for gn in graph_nodes.values():
            self.add_graph_node(gn)

    def remove_graph_nodes(self, graph_nodes: dict[str, GraphNode]) -> None:
        for gn in graph_nodes.keys():
            self.graph_nodes.pop(gn, None)

    def to_mermaid_js_code(self) -> str:
        code = f"graph TB\n"

        for graph_node in self.graph_nodes.values():
            code += graph_node.to_mermaid_js_code()

        code += self.styles

        return code

    def to_diagrams(self) -> None:
        with Diagram(self.title, show=False, filename="diagrams/diagram", direction="TB"):
            if self.graph_nodes is not None:
                for graph_node in self.graph_nodes.values():
                    graph_node.to_diagrams()


class SubGraph(GraphNode, Graph):
    def to_mermaid_js_code(self) -> str:
        if self.graph_nodes is None:
            return ""

        code = f"subgraph \"{self.prefix}: {self.name}\"\n"

        for graph_node in self.graph_nodes.values():
            code += graph_node.to_mermaid_js_code()

        code += f"end\n"

        return code

    def to_diagrams(self) -> None:
        graph_attr = {}
        if self.color is not None:
            graph_attr["bgcolor"] = self.color

        with Cluster(f"{self.prefix}: {self.name}", graph_attr=graph_attr):
            for graph_node in self.graph_nodes.values():
                graph_node.to_diagrams()
