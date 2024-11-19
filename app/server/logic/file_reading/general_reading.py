from pathlib import Path
from typing import Callable, Sequence

import pandas as pd

from .processing_interface import FileProcessingStrategy


def processing_placeholder(line: str):
    return line


class TEXTFile(FileProcessingStrategy):
    def __init__(self, file_path, processing_function=processing_placeholder):
        self._file_path: Path = file_path
        self._process: Callable[[str], Sequence | dict] = processing_function

    def get_reader(self, file_stream):
        return file_stream

    def set_headers(self, reader):
        self._headers = []

    def process_row(self, line):
        return line

    def get_dataframe(self):
        # this is more of an placeholer solution
        result = []
        with open(self._file_path, encoding="utf-8") as file:
            for row in file:
                result.append(self._process(row))

        return pd.DataFrame(result)

    def get_type_hint(self):
        return "The edge is a string unless a specified preprocessing method has been supplied. In the latter case the format of the edge matches the return of the preprocessing method"
