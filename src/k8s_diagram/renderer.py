import base64
import io
from typing import Protocol

import requests
from PIL import Image
from matplotlib import pyplot as plt

from k8s_diagram.types.base import Graph


class RendererProtocol(Protocol):
    def render(self): ...


class BaseRenderer:
    def __init__(self, graph: Graph):
        self.graph = graph


class MermaidJSRenderer(BaseRenderer):
    @property
    def graph_code(self) -> str:
        return self.graph.to_mermaid_js_code()

    def render(self):
        graphbytes = self.graph_code.encode("ascii")

        base64_bytes = base64.b64encode(graphbytes)
        base64_string = base64_bytes.decode("ascii")

        path = f"https://mermaid.ink/img/{base64_string}"
        content = requests.get(path).content
        image_bytes = io.BytesIO(content)
        img = Image.open(image_bytes)
        plt.imshow(img)
        plt.show()


class DiagramsRenderer(BaseRenderer):
    def render(self):
        self.graph.to_diagrams()
