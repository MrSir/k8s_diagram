from k8s_diagram.types import Namespace, Graph


def parse_dictionary(data: dict) -> Graph:
    graph = Graph()

    for namespace_dict in data['namespaces']:
        namespace = Namespace.from_dict(namespace_dict)

        graph.add_namespace(namespace)

    return graph
