from processing_interface import FileProcessingStrategy
from scipy.io import mmread, mminfo
import pandas as pd
from pathlib import Path



class MTXFile(FileProcessingStrategy):
    def __init__(self, file_path):
        self._file_path : Path = file_path


    def get_reader(self, file_stream):
        return file_stream
    
    def set_headers(self, reader):

        # opening the same file multiple times in one process is safe (using the dafult read-only mode)
        # each time a new file object iterator is created - no shared state between them exists

        # checking the header and comment count and iterating the main reader accordingly
        with open(self._file_path) as file:
            comment_count = 1
            for line in file:
                if line.startswith('%'):
                    comment_count +=1
                    continue
                else:
                    break

        for _ in range(comment_count):
            next(reader)

        self._headers = mminfo(self._file_path)
    

    def process_row(self, line: str):
        # currently the formatting is based on the demo datasets, might not encapsulate all .mtx possibilities
        split_line = line.rstrip().split(" ")
        result = (0,0)
        if len(split_line) == 2:
            result = (int(split_line[0]), int(split_line[1]))
        elif len(split_line) == 3:
            result = (int(split_line[0]), int(split_line[1]), float(split_line[2]))
        return result


    def get_dataframe(self):
        matrix = mmread(self._file_path)
        dense_matrix = matrix.todense() # type: ignore

        return pd.DataFrame(dense_matrix)
    
    def get_type_hint(self):
        return "The given edge is a tuple. Access its data by indexing : 0 - source node, 1 - destination node, (optionally) 2 - weight of the edge."