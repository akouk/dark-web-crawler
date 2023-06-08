from typing import TypedDict


class ConfigProject(TypedDict):
    """
    A TypedDict representing the project section of the configuration.
    """
    name: str
    directory: str


class ConfigRequest(TypedDict):
    """
    A TypedDict representing the request section of the configuration.
    """
    timeout: int


class ConfigProxies(TypedDict):
    """
    A TypedDict representing the proxies section of the configuration.
    """
    http: str
    https: str


class ConfigDict(TypedDict):
    """
    A TypedDict representing the entire configuration.
    """
    project: ConfigProject
    base_url: str
    num_worker_threads: int
    request: ConfigRequest
    proxies: ConfigProxies
