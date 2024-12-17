from csv import DictReader
from io import TextIOWrapper
from pathlib import Path

from .processing_interface import FileProcessingStrategy


class CSVFile(FileProcessingStrategy):
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def get_reader(self, file_stream: TextIOWrapper) -> DictReader[str]:
        return DictReader(file_stream)

    def set_headers(self, reader: DictReader[str]) -> None:
        self._headers = reader.fieldnames

    def process_row(self, row: dict) -> dict:
        return row
