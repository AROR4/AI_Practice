from abc import ABC
from abc import abstractmethod


class BaseMCPProvider(ABC):

    @abstractmethod
    def search(
        self,
        query: str
    ) -> str:
        """
        Search enterprise knowledge source.
        """
        pass