import uuid
from dataclasses import dataclass
from typing import Self


@dataclass
class Service:
    name: str
    app: str
    indent: str = "      "

    def to_graph(self) -> str:
        graph = f"{self.indent}ser_{uuid.uuid4()}[\"{self.name}\"]\n"

        return graph


@dataclass
class Pod:
    name: str
    app: str
    indent: str = "      "
    image: str = "<img src='data:image/svg+xml;base64,PHN2ZyB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOmNjPSJodHRwOi8vY3JlYXRpdmVjb21tb25zLm9yZy9ucyMiIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyIgeG1sbnM6c3ZnPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczpzb2RpcG9kaT0iaHR0cDovL3NvZGlwb2RpLnNvdXJjZWZvcmdlLm5ldC9EVEQvc29kaXBvZGktMC5kdGQiIHhtbG5zOmlua3NjYXBlPSJodHRwOi8vd3d3Lmlua3NjYXBlLm9yZy9uYW1lc3BhY2VzL2lua3NjYXBlIiB3aWR0aD0iMTguMDM1MzM0bW0iIGhlaWdodD0iMTcuNTAwMzc4bW0iIHZpZXdCb3g9IjAgMCAxOC4wMzUzMzQgMTcuNTAwMzc4IiB2ZXJzaW9uPSIxLjEiIGlkPSJzdmcxMzgyNiIgaW5rc2NhcGU6dmVyc2lvbj0iMC45MSByMTM3MjUiIHNvZGlwb2RpOmRvY25hbWU9InBvZC5zdmciPiYjeGE7ICA8ZGVmcyBpZD0iZGVmczEzODIwIi8+JiN4YTsgIDxzb2RpcG9kaTpuYW1lZHZpZXcgaWQ9ImJhc2UiIHBhZ2Vjb2xvcj0iI2ZmZmZmZiIgYm9yZGVyY29sb3I9IiM2NjY2NjYiIGJvcmRlcm9wYWNpdHk9IjEuMCIgaW5rc2NhcGU6cGFnZW9wYWNpdHk9IjAuMCIgaW5rc2NhcGU6cGFnZXNoYWRvdz0iMiIgaW5rc2NhcGU6em9vbT0iOCIgaW5rc2NhcGU6Y3g9IjE2Ljg0NzQ5NiIgaW5rc2NhcGU6Y3k9IjMzLjc1MjIzOSIgaW5rc2NhcGU6ZG9jdW1lbnQtdW5pdHM9Im1tIiBpbmtzY2FwZTpjdXJyZW50LWxheWVyPSJsYXllcjEiIHNob3dncmlkPSJmYWxzZSIgaW5rc2NhcGU6d2luZG93LXdpZHRoPSIxNDQwIiBpbmtzY2FwZTp3aW5kb3ctaGVpZ2h0PSI3NzUiIGlua3NjYXBlOndpbmRvdy14PSIwIiBpbmtzY2FwZTp3aW5kb3cteT0iMSIgaW5rc2NhcGU6d2luZG93LW1heGltaXplZD0iMSIgZml0LW1hcmdpbi10b3A9IjAiIGZpdC1tYXJnaW4tbGVmdD0iMCIgZml0LW1hcmdpbi1yaWdodD0iMCIgZml0LW1hcmdpbi1ib3R0b209IjAiLz4mI3hhOyAgPG1ldGFkYXRhIGlkPSJtZXRhZGF0YTEzODIzIj4mI3hhOyAgICA8cmRmOlJERj4mI3hhOyAgICAgIDxjYzpXb3JrIHJkZjphYm91dD0iIj4mI3hhOyAgICAgICAgPGRjOmZvcm1hdD5pbWFnZS9zdmcreG1sPC9kYzpmb3JtYXQ+JiN4YTsgICAgICAgIDxkYzp0eXBlIHJkZjpyZXNvdXJjZT0iaHR0cDovL3B1cmwub3JnL2RjL2RjbWl0eXBlL1N0aWxsSW1hZ2UiLz4mI3hhOyAgICAgICAgPGRjOnRpdGxlLz4mI3hhOyAgICAgIDwvY2M6V29yaz4mI3hhOyAgICA8L3JkZjpSREY+JiN4YTsgIDwvbWV0YWRhdGE+JiN4YTsgIDxnIGlua3NjYXBlOmxhYmVsPSJDYWxxdWUgMSIgaW5rc2NhcGU6Z3JvdXBtb2RlPSJsYXllciIgaWQ9ImxheWVyMSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTAuOTkyNjI2MzgsLTEuMTc0MTgxKSI+JiN4YTsgICAgPGcgaWQ9Imc3MCIgdHJhbnNmb3JtPSJtYXRyaXgoMS4wMTQ4ODg3LDAsMCwxLjAxNDg4ODcsMTYuOTAyMTQ2LC0yLjY5ODcyNikiPiYjeGE7ICAgICAgPHBhdGggaW5rc2NhcGU6ZXhwb3J0LXlkcGk9IjI1MC41NSIgaW5rc2NhcGU6ZXhwb3J0LXhkcGk9IjI1MC41NSIgaW5rc2NhcGU6ZXhwb3J0LWZpbGVuYW1lPSJuZXcucG5nIiBpbmtzY2FwZTpjb25uZWN0b3ItY3VydmF0dXJlPSIwIiBpZD0icGF0aDMwNTUiIGQ9Im0gLTYuODQ5MjAxNSw0LjI3MjQ2NjggYSAxLjExOTEyNTUsMS4xMDk5NjcxIDAgMCAwIC0wLjQyODg4MTgsMC4xMDg1MzAzIGwgLTUuODUyNDAzNywyLjc5NjMzOTQgYSAxLjExOTEyNTUsMS4xMDk5NjcxIDAgMCAwIC0wLjYwNTUyNCwwLjc1Mjk3NTkgbCAtMS40NDM4MjgsNi4yODEyODQ2IGEgMS4xMTkxMjU1LDEuMTA5OTY3MSAwIDAgMCAwLjE1MTk0MywwLjg1MTAyOCAxLjExOTEyNTUsMS4xMDk5NjcxIDAgMCAwIDAuMDYzNjIsMC4wODgzMiBsIDQuMDUwOCw1LjAzNjU1NSBhIDEuMTE5MTI1NSwxLjEwOTk2NzEgMCAwIDAgMC44NzQ5NzksMC40MTc2NTQgbCA2LjQ5NjEwMTEsLTAuMDAxNSBhIDEuMTE5MTI1NSwxLjEwOTk2NzEgMCAwIDAgMC44NzQ5Nzg4LC0wLjQxNjkwNiBMIDEuMzgxODg3MiwxNS4xNDk0NTMgQSAxLjExOTEyNTUsMS4xMDk5NjcxIDAgMCAwIDEuNTk4MTk4NiwxNC4yMTAxMDQgTCAwLjE1MjEyNjU3LDcuOTI4ODE1NCBBIDEuMTE5MTI1NSwxLjEwOTk2NzEgMCAwIDAgLTAuNDUzMzk3OTQsNy4xNzU4Mzk2IEwgLTYuMzA2NTQ5Niw0LjM4MDk5NzEgQSAxLjExOTEyNTUsMS4xMDk5NjcxIDAgMCAwIC02Ljg0OTIwMTUsNC4yNzI0NjY4IFoiIHN0eWxlPSJmaWxsOiMzMjZjZTU7ZmlsbC1vcGFjaXR5OjE7c3Ryb2tlOm5vbmU7c3Ryb2tlLXdpZHRoOjA7c3Ryb2tlLW1pdGVybGltaXQ6NDtzdHJva2UtZGFzaGFycmF5Om5vbmU7c3Ryb2tlLW9wYWNpdHk6MSIvPiYjeGE7ICAgICAgPHBhdGggaWQ9InBhdGgzMDU0LTItOSIgZD0iTSAtNi44NTIzNDM1LDMuODE3NjM3MiBBIDEuMTgxNDMwNCwxLjE3MTc2MiAwIDAgMCAtNy4zMDQ0Mjg0LDMuOTMyOTA0IGwgLTYuMTc4NzQyNiwyLjk1MTI3NTggYSAxLjE4MTQzMDQsMS4xNzE3NjIgMCAwIDAgLTAuNjM5MjA2LDAuNzk0ODkxIGwgLTEuNTIzOTE1LDYuNjMwODI4MiBhIDEuMTgxNDMwNCwxLjE3MTc2MiAwIDAgMCAwLjE2MDE3NSwwLjg5ODkzIDEuMTgxNDMwNCwxLjE3MTc2MiAwIDAgMCAwLjA2NzM2LDAuMDkyODEgbCA0LjI3NjA5NCw1LjMxNzIzNiBhIDEuMTgxNDMwNCwxLjE3MTc2MiAwIDAgMCAwLjkyMzYzLDAuNDQwODU4IGwgNi44NTc2MTg4LC0wLjAwMTUgYSAxLjE4MTQzMDQsMS4xNzE3NjIgMCAwIDAgMC45MjM2MzA4LC0wLjQ0MDExIGwgNC4yNzQ1OTY2LC01LjMxNzk4NSBhIDEuMTgxNDMwNCwxLjE3MTc2MiAwIDAgMCAwLjIyODI4OCwtMC45OTA5OTMgTCAwLjUzODk0NDM5LDcuNjc3NTczOCBBIDEuMTgxNDMwNCwxLjE3MTc2MiAwIDAgMCAtMC4xMDAyNjEwMSw2Ljg4MzQzMTMgTCAtNi4yNzkwMDM3LDMuOTMyMTU1NSBBIDEuMTgxNDMwNCwxLjE3MTc2MiAwIDAgMCAtNi44NTIzNDM1LDMuODE3NjM3MiBaIG0gMC4wMDI5OSwwLjQ1NTA3ODkgYSAxLjExOTEyNTUsMS4xMDk5NjcxIDAgMCAxIDAuNTQyNjUxNywwLjEwODUzMDMgbCA1Ljg1MzE1MTY5LDIuNzk0ODQyNSBBIDEuMTE5MTI1NSwxLjEwOTk2NzEgMCAwIDEgMC4xNTE5NzgxMSw3LjkyOTA2NDggTCAxLjU5ODA1MSwxNC4yMTAzNSBhIDEuMTE5MTI1NSwxLjEwOTk2NzEgMCAwIDEgLTAuMjE2MzEyMywwLjkzOTM0OCBsIC00LjA0OTMwMzIsNS4wMzczMDQgYSAxLjExOTEyNTUsMS4xMDk5NjcxIDAgMCAxIC0wLjg3NDk3ODksMC40MTY5MDYgbCAtNi40OTYxMDA2LDAuMDAxNSBhIDEuMTE5MTI1NSwxLjEwOTk2NzEgMCAwIDEgLTAuODc0OTc5LC0wLjQxNzY1MiBsIC00LjA1MDgsLTUuMDM2NTU0IGEgMS4xMTkxMjU1LDEuMTA5OTY3MSAwIDAgMSAtMC4wNjM2MiwtMC4wODgzMiAxLjExOTEyNTUsMS4xMDk5NjcxIDAgMCAxIC0wLjE1MTk0MiwtMC44NTEwMjggbCAxLjQ0MzgyNywtNi4yODEyODUzIGEgMS4xMTkxMjU1LDEuMTA5OTY3MSAwIDAgMSAwLjYwNTUyNCwtMC43NTI5NzU4IGwgNS44NTI0MDM2LC0yLjc5NjMzOTUgYSAxLjExOTEyNTUsMS4xMDk5NjcxIDAgMCAxIDAuNDI4ODgxOSwtMC4xMDg1MzAzIHoiIHN0eWxlPSJjb2xvcjojMDAwMDAwO2ZvbnQtc3R5bGU6bm9ybWFsO2ZvbnQtdmFyaWFudDpub3JtYWw7Zm9udC13ZWlnaHQ6bm9ybWFsO2ZvbnQtc3RyZXRjaDpub3JtYWw7Zm9udC1zaXplOm1lZGl1bTtsaW5lLWhlaWdodDpub3JtYWw7Zm9udC1mYW1pbHk6U2FuczstaW5rc2NhcGUtZm9udC1zcGVjaWZpY2F0aW9uOlNhbnM7dGV4dC1pbmRlbnQ6MDt0ZXh0LWFsaWduOnN0YXJ0O3RleHQtZGVjb3JhdGlvbjpub25lO3RleHQtZGVjb3JhdGlvbi1saW5lOm5vbmU7bGV0dGVyLXNwYWNpbmc6bm9ybWFsO3dvcmQtc3BhY2luZzpub3JtYWw7dGV4dC10cmFuc2Zvcm06bm9uZTt3cml0aW5nLW1vZGU6bHItdGI7ZGlyZWN0aW9uOmx0cjtiYXNlbGluZS1zaGlmdDpiYXNlbGluZTt0ZXh0LWFuY2hvcjpzdGFydDtkaXNwbGF5OmlubGluZTtvdmVyZmxvdzp2aXNpYmxlO3Zpc2liaWxpdHk6dmlzaWJsZTtmaWxsOiNmZmZmZmY7ZmlsbC1vcGFjaXR5OjE7ZmlsbC1ydWxlOm5vbnplcm87c3Ryb2tlOm5vbmU7c3Ryb2tlLXdpZHRoOjA7c3Ryb2tlLW1pdGVybGltaXQ6NDtzdHJva2UtZGFzaGFycmF5Om5vbmU7bWFya2VyOm5vbmU7ZW5hYmxlLWJhY2tncm91bmQ6YWNjdW11bGF0ZSIgaW5rc2NhcGU6Y29ubmVjdG9yLWN1cnZhdHVyZT0iMCIvPiYjeGE7ICAgIDwvZz4mI3hhOyAgICA8dGV4dCBpZD0idGV4dDIwNjYiIHk9IjE2LjgxMTc3NSIgeD0iMTAuMDE3MTgzIiBzdHlsZT0iZm9udC1zdHlsZTpub3JtYWw7Zm9udC13ZWlnaHQ6bm9ybWFsO2ZvbnQtc2l6ZToxMC41ODMzMzMwMnB4O2xpbmUtaGVpZ2h0OjYuNjE0NTgzNDlweDtmb250LWZhbWlseTpTYW5zO2xldHRlci1zcGFjaW5nOjBweDt3b3JkLXNwYWNpbmc6MHB4O2ZpbGw6I2ZmZmZmZjtmaWxsLW9wYWNpdHk6MTtzdHJva2U6bm9uZTtzdHJva2Utd2lkdGg6MC4yNjQ1ODMzMnB4O3N0cm9rZS1saW5lY2FwOmJ1dHQ7c3Ryb2tlLWxpbmVqb2luOm1pdGVyO3N0cm9rZS1vcGFjaXR5OjEiIHhtbDpzcGFjZT0icHJlc2VydmUiPjx0c3BhbiBzdHlsZT0iZm9udC1zdHlsZTpub3JtYWw7Zm9udC12YXJpYW50Om5vcm1hbDtmb250LXdlaWdodDpub3JtYWw7Zm9udC1zdHJldGNoOm5vcm1hbDtmb250LXNpemU6Mi44MjIyMjIyM3B4O2ZvbnQtZmFtaWx5OkFyaWFsOy1pbmtzY2FwZS1mb250LXNwZWNpZmljYXRpb246J0FyaWFsLCBOb3JtYWwnO3RleHQtYWxpZ246Y2VudGVyO3dyaXRpbmctbW9kZTpsci10Yjt0ZXh0LWFuY2hvcjptaWRkbGU7ZmlsbDojZmZmZmZmO2ZpbGwtb3BhY2l0eToxO3N0cm9rZS13aWR0aDowLjI2NDU4MzMycHgiIHk9IjE2LjgxMTc3NSIgeD0iMTAuMDE3MTgzIiBpZD0idHNwYW4yMDY0IiBzb2RpcG9kaTpyb2xlPSJsaW5lIj5wb2Q8L3RzcGFuPjwvdGV4dD4mI3hhOyAgICA8ZyBpZD0iZzMzNDEiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAuMTI3NjY2NjEsMCkiPiYjeGE7ICAgICAgPHBhdGggaW5rc2NhcGU6ZXhwb3J0LXlkcGk9IjM3Ni41Nzk5OSIgaW5rc2NhcGU6ZXhwb3J0LXhkcGk9IjM3Ni41Nzk5OSIgc3R5bGU9ImZpbGw6I2ZmZmZmZjtmaWxsLXJ1bGU6ZXZlbm9kZDtzdHJva2U6bm9uZTtzdHJva2Utd2lkdGg6MC4yNjQ1ODMzMjtzdHJva2UtbGluZWNhcDpzcXVhcmU7c3Ryb2tlLW1pdGVybGltaXQ6MTAiIGlua3NjYXBlOmNvbm5lY3Rvci1jdXJ2YXR1cmU9IjAiIGQ9Ik0gNi4yNjE3OTE0LDcuMDM2MDg2IDkuODgyNjMxNyw1Ljk4NjA4NyAxMy41MDM0NjIsNy4wMzYwODYgOS44ODI2MzE3LDguMDg2MDg3IFoiIGlkPSJwYXRoOTEwIi8+JiN4YTsgICAgICA8cGF0aCBpbmtzY2FwZTpleHBvcnQteWRwaT0iMzc2LjU3OTk5IiBpbmtzY2FwZTpleHBvcnQteGRwaT0iMzc2LjU3OTk5IiBzdHlsZT0iZmlsbDojZmZmZmZmO2ZpbGwtcnVsZTpldmVub2RkO3N0cm9rZTpub25lO3N0cm9rZS13aWR0aDowLjI2NDU4MzMyO3N0cm9rZS1saW5lY2FwOnNxdWFyZTtzdHJva2UtbWl0ZXJsaW1pdDoxMCIgaW5rc2NhcGU6Y29ubmVjdG9yLWN1cnZhdHVyZT0iMCIgZD0ibSA2LjI2MTc5MTQsNy40MzgxNyAwLDMuODUyNzc4IDMuMzczNjEwMywxLjg2ODc0OSAwLjAxNjcsLTQuNzEzMTkzIHoiIGlkPSJwYXRoOTEyIi8+JiN4YTsgICAgICA8cGF0aCBpbmtzY2FwZTpleHBvcnQteWRwaT0iMzc2LjU3OTk5IiBpbmtzY2FwZTpleHBvcnQteGRwaT0iMzc2LjU3OTk5IiBzdHlsZT0iZmlsbDojZmZmZmZmO2ZpbGwtcnVsZTpldmVub2RkO3N0cm9rZTpub25lO3N0cm9rZS13aWR0aDowLjI2NDU4MzMyO3N0cm9rZS1saW5lY2FwOnNxdWFyZTtzdHJva2UtbWl0ZXJsaW1pdDoxMCIgaW5rc2NhcGU6Y29ubmVjdG9yLWN1cnZhdHVyZT0iMCIgZD0ibSAxMy41MDM0NjIsNy40MzgxNyAwLDMuODUyNzc4IC0zLjM3MzYxLDEuODY4NzQ5IC0wLjAxNjcsLTQuNzEzMTkzIHoiIGlkPSJwYXRoOTE0Ii8+JiN4YTsgICAgPC9nPiYjeGE7ICA8L2c+JiN4YTs8L3N2Zz4=' />"

    @property
    def graph_name(self) -> str:
        return f"{self.indent}pod_{uuid.uuid4()}"

    @property
    def graph_title(self) -> str:
        return f"<span>{self.name}</span>"

    def to_graph(self) -> str:
        graph = f"{self.graph_name}({self.image}{self.graph_title})\n"

        return graph


@dataclass
class App:
    name: str
    services: list[Service] | None = None
    pods: list[Pod] | None = None
    indent: str = "    "

    def to_graph(self) -> str:
        graph = f"{self.indent}subgraph App: {self.name}\n"

        for service in self.services:
            graph += service.to_graph()

        for pod in self.pods:
            graph += pod.to_graph()

        graph += f"{self.indent}end\n"

        return graph


@dataclass
class Namespace:
    name: str
    apps: list[App] | None = None
    indent: str = "  "

    def to_graph(self) -> str:
        graph = f"{self.indent}subgraph Namespace: {self.name}\n"

        if self.apps is not None:
            for app in self.apps:
                graph += app.to_graph()

        graph += f"{self.indent}end\n"

        return graph

    @classmethod
    def from_dict(cls, dictionary: dict) -> Self:
        service_apps = {s['app'] for s in dictionary["services"]}
        pod_apps = {p['app'] for p in dictionary["pods"]}

        app_names = service_apps.union(pod_apps)

        apps = []

        for app_name in app_names:
            app = App(name=app_name)
            app.services = [Service(name=s['name'], app=app_name) for s in dictionary['services'] if s['app'] == app_name]
            app.pods = [Pod(name=p['name'], app=app_name) for p in dictionary['pods'] if p['app'] == app_name]
            apps.append(app)

        return cls(name=dictionary['name'], apps=apps)


@dataclass
class Graph:
    namespaces: list[Namespace] | None = None

    def add_namespace(self, namespace: Namespace) -> None:
        if self.namespaces is None:
            self.namespaces = []

        self.namespaces.append(namespace)

    def to_mermaid_js_code(self) -> str:
        graph = f"graph TD\n"

        for namespace in self.namespaces:
            graph += namespace.to_graph()

        return graph
