from .processing_interface import FileProcessingStrategy
import csv
import pandas as pd


class CSVFile(FileProcessingStrategy):
    def __init__(self, file_path):
        self._file_path = file_path


    def get_reader(self, file_stream):
        reader = csv.DictReader(file_stream)
        return reader
    
    def set_headers(self, reader ):
        self._headers = reader.fieldnames
    
    def process_row(self, line):
        return line

    def get_dataframe(self):
        return pd.read_csv(self._file_path)
    
    def get_type_hint(self):
        return "The edge is a dictionary. Its keys are the headers of the supplied .csv file."
     

    
