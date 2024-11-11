import csv
import importlib.util
import inspect
import os
import sys
import time
from pathlib import Path
import psutil

import pandas as pd


def get_class_instance_from(file_path: Path) -> object:
    module_name = os.path.basename(file_path)

    spec = importlib.util.spec_from_file_location(str(file_path), file_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore

    for name_local in dir(module):
        if not inspect.isclass(getattr(module, name_local)):
            continue
        MysteriousClass = getattr(module, name_local)
        if not inspect.isabstract(MysteriousClass):
            return MysteriousClass()


class Runner:
    def __init__(
        self,
        dataset_path: Path,
        streaming_path: Path,
        preprocess_path: Path = Path(""),
        batch_path: Path = Path(""),
    ):
        self._dataset = dataset_path
        self._should_preprocess = not preprocess_path
        self._with_batch = not batch_path.name is None
        print(self._with_batch)

        if self._should_preprocess:
            self._preprocess = get_class_instance_from(preprocess_path)

        self._stream = get_class_instance_from(streaming_path)

        if self._with_batch:
            self._batch = get_class_instance_from(batch_path)
        print(self._batch)
        # time inverals are now saved using the perf_counter_ns for greater precision 
        self._calculation_time_per_edge = []
        self._preprocessing_time_per_edge = []
                
        # Saves the amount of stored memory in RAM (non-swapped) in MB by this runner process 
        # - will include everything including the sizes of the history and of the stream, batch object
        # stop recording when the streaming algorithm is done computing 
        self._memory_history = []
        self._number_of_processed_edges = 0


    # getters for metrics and results - 
    # some of them are optional (like results from batch) => changed method tuple return to getters
    @property
    def calculation_time_per_edge(self):
        return self._calculation_time_per_edge
    
    @property
    def preprocessing_time_per_edge(self):
        return self._preprocessing_time_per_edge
    
    @property
    def memory_history(self):
        return self._memory_history
    
    
    def get_stream_results(self):
        return self._stream.submit_results() # type: ignore
    
    def get_batch_results(self):
        return self._batch.submit_results() # type: ignore
    

    def get_streaming_accuracy(self):
        streaming_results = self._stream.submit_results()
        batch_results = self._batch.submit_results()
        correct = 0
        for stream, batch in zip(streaming_results, batch_results):
            if stream[0] == batch[0]:
                correct +=1

        return correct/len(streaming_results)


    def run(self):
        process = psutil.Process(os.getpid())
        columns = [
            "",
            "company",
            "line",
            "departure_time",
            "arrival_time",
            "start",
            "end",
            "start_lat",
            "start_lon",
            "end_lat",
            "end_lon",
        ]

        MB_ratio = 1/(1024*1024) 
        self._memory_history = [process.memory_info().rss*MB_ratio]
        
        with open(self._dataset, encoding="utf-8") as file:
            reader = csv.DictReader(
                file, fieldnames=columns
            )  
            next(reader, None)

            for row in reader:
                self._number_of_processed_edges += 1

                if self._should_preprocess:
                    preprocess_start = time.perf_counter_ns()
                    row = self._preprocess.create_edge_from(row)
                    preprocess_end = time.perf_counter_ns()
                    preprocess_duration = preprocess_end - preprocess_start
                    self._preprocessing_time_per_edge.append(
                        preprocess_duration
                    )

                property_start = time.perf_counter_ns()
                self._stream.on_edge_calculate(row)  # type: ignore
                property_end = time.perf_counter_ns()


                property_calculation_duration = property_end - property_start
                self._calculation_time_per_edge.append(
                    property_calculation_duration 
                )

                self._memory_history.append(process.memory_info().rss*MB_ratio)


            if self._with_batch:
                if os.path.basename(self._dataset).endswith(".csv"):
                    self._batch.calculate_property(pd.read_csv(self._dataset))  # type: ignore

                elif os.path.basename(self._dataset).endswith(".mtx"):
                    # TODO: convert mtx to dataframe
                    pass

                else:
                    # TODO: how to make it possible to batch process when the best we got is some text file
                    # batch processing atm requires a pandas DataFrame
                    pass

