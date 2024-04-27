import uuid
from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class GraphNode:
    prefix: str
    name: str
    __id: str | None = None

    @property
    def id(self) -> str:
        if self.__id is None:
            self.__id = f"{self.prefix}_{uuid.uuid4()}"

        return self.__id

    def to_mermaid_js_code(self) -> str:
        return f"{self.id}(\"{self.name}\")\n"


@dataclass
class Graph:
    graph_nodes: list[GraphNode] | None = None

    def add_graph_node(self, graph_node: GraphNode) -> None:
        if self.graph_nodes is None:
            self.graph_nodes = []

        self.graph_nodes.append(graph_node)

    def to_mermaid_js_code(self) -> str:
        code = f"graph TD\n"

        for graph_node in self.graph_nodes:
            code += graph_node.to_mermaid_js_code()

        return code


@dataclass
class SubGraph(GraphNode, Graph):
    def to_mermaid_js_code(self) -> str:
        code = f"subgraph {self.prefix}: {self.name}\n"

        if self.graph_nodes is not None:
            for graph_node in self.graph_nodes:
                code += graph_node.to_mermaid_js_code()

        code += f"end\n"

        return code



