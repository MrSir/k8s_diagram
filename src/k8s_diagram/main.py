import base64
import requests
import io
from PIL import Image
import matplotlib.pyplot as plt


def display_graph(graph: str):
    graphbytes = graph.encode("ascii")

    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")

    path = f"https://mermaid.ink/img/{base64_string}"
    content = requests.get(path).content
    image_bytes = io.BytesIO(content)
    img = Image.open(image_bytes)
    plt.imshow(img)
    plt.show()


# graph = """
#     graph LR;
#         A--> B & C & D;
#         B--> A & E;
#         C--> A & E;
#         D--> A & E;
#         E--> B & C & D;
#     """
#
# display_graph(graph)

# display_graph(graph.to_mermaid_js_code())