from .base import PipelineBase as PipelineBase
from .base import StatsClientBase as StatsClientBase

class Pipeline(PipelineBase):
    def __init__(self, client: StatsClientBase) -> None: ...

class StatsClient(StatsClientBase):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8125,
        prefix: str | None = None,
        maxudpsize: int = 512,
        ipv6: bool = False,
    ) -> None: ...
    def close(self) -> None: ...
    def pipeline(self) -> Pipeline: ...
