from abc import ABC, abstractmethod


class FileProcessingStrategy(ABC):
    @abstractmethod
    def get_reader(self, file_stream): ...

    @abstractmethod
    def get_type_hint(self): ...

    # @abstractmethod
    # def skip_header_lines(self, reader):
    #     ...

    @abstractmethod
    def set_headers(self, reader): ...

    @abstractmethod
    def process_row(self, line): ...

    @abstractmethod
    def get_dataframe(self): ...
