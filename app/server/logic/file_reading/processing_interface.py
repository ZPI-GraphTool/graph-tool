from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import Any


class FileProcessingStrategy(ABC):
    @abstractmethod
    def get_reader(self, file_stream: TextIOWrapper) -> Any: ...

    @abstractmethod
    def set_headers(self, reader: Any) -> None: ...

    @abstractmethod
    def process_row(self, row: Any) -> Any: ...

    # @abstractmethod
    # def get_dataframe(self, lst: list) -> pd.DataFrame:
    #     ...
