from typing import TypedDict


class ConfigProject(TypedDict):
    name: str
    directory: str


class ConfigRequest(TypedDict):
    timeout: int


class ConfigProxies(TypedDict):
    http: str
    https: str


class ConfigDict(TypedDict):
    project: ConfigProject
    base_url: str
    num_worker_threads: int
    request: ConfigRequest
    proxies: ConfigProxies
