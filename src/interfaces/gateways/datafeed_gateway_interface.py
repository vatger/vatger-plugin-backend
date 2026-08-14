from abc import ABC, abstractmethod

from datafeed.datafeed import DatafeedModel


class DatafeedGatewayInterface(ABC):
    @abstractmethod
    async def fetch(self) -> DatafeedModel | None: ...
