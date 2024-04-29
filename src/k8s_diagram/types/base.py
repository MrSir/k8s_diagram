import uuid
from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class GraphNode:
    prefix: str
    name: str
    uid: str
    namespace: str | None = None
    css_class: str | None = None
    __id: str | None = None

    @property
    def id(self) -> str:
        if self.__id is None:
            self.__id = f"{self.prefix}{self.uid}"

        return self.__id

    def to_mermaid_js_code(self) -> str:
        style = ""
        if self.css_class is not None:
            style += f":::{self.css_class}"

        return f"{self.id}(\"{self.name}\"){style}\n"


@dataclass
class Graph:
    graph_nodes: list[GraphNode] | None = None

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
            self.graph_nodes = []

        self.graph_nodes.append(graph_node)

    def to_mermaid_js_code(self) -> str:
        code = f"graph TB\n"

        for graph_node in self.graph_nodes:
            code += graph_node.to_mermaid_js_code()

        code += self.styles

        return code


class SubGraph(GraphNode, Graph):
    def to_mermaid_js_code(self) -> str:
        if self.graph_nodes is None:
            return ""

        code = f"subgraph \"{self.prefix}: {self.name}\"\n"

        for graph_node in self.graph_nodes:
            code += graph_node.to_mermaid_js_code()

        code += f"end\n"

        return code
