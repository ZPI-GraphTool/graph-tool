from io import TextIOWrapper
from pathlib import Path
from typing import Callable, Sequence

import pandas as pd

from .processing_interface import FileProcessingStrategy


class TEXTFile(FileProcessingStrategy):
    def __init__(
        self, file_path: Path
    ) -> None:
        self._file_path = file_path

    def get_reader(self, file_stream: TextIOWrapper) -> TextIOWrapper:
        return file_stream

    def set_headers(self, reader: TextIOWrapper) -> None:
        self._headers = []

    def process_row(self, row: str) -> str:
        return row

