from io import TextIOWrapper
from pathlib import Path

from scipy.io import mminfo

from .processing_interface import FileProcessingStrategy


class MTXFile(FileProcessingStrategy):
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def get_reader(self, file_stream: TextIOWrapper) -> TextIOWrapper:
        return file_stream

    def set_headers(self, reader: TextIOWrapper) -> None:
        # opening the same file multiple times in one process is safe (using the default read-only mode)
        # each time a new file object iterator is created - no shared state between them exists

        # checking the header and comment count and iterating the main reader accordingly
        with open(self._file_path) as file:
            comment_count = 1
            for line in file:
                if line.startswith("%"):
                    comment_count += 1
                    continue
                else:
                    break

        for _ in range(comment_count):
            next(reader)

        self._headers = mminfo(self._file_path)

    def process_row(self, row: str) -> tuple[int, int] | tuple[int, int, float]:
        # currently the formatting is based on the demo datasets, might not encapsulate all .mtx possibilities
        split_row = row.rstrip().split(" ")
        result = (0, 0)
        if len(split_row) == 2:
            result = (int(split_row[0]), int(split_row[1]), 1.0)
        elif len(split_row) == 3:
            result = (int(split_row[0]), int(split_row[1]), float(split_row[2]))
        return result

    # def get_dataframe(self, lst) -> pd.DataFrame:
    # matrix = mmread(self._file_path)

    # lst = []
    # for i in range(len(matrix.nonzero()[0])):
    #     data = (matrix.nonzero()[0][i], matrix.nonzero()[1][i], matrix.data[i])
    #     if self._process:
    #         data = self._process(data)
    # lst.append(data)

    # return pd.DataFrame(lst)
