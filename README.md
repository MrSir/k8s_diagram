# k8s_diagram
A simple package to generate mermaid.js diagram of your Kubernetes Cluster


## Use

```python
from k8s_diagram.main import K8sDiagrammer


endpoint = "<kubernetes api endpoint>"
cert_path = "<ssl cert file path>"
api_key = "<api key>"
excluded_namespaces = {
    "default",
    "kube-system",
}

diagrammer = K8sDiagrammer(endpoint, api_key, cert_path=cert_path, excluded_namespaces=excluded_namespaces)
print(diagrammer.renderer().graph_code)
diagrammer.render()

```
