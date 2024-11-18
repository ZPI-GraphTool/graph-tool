import csv
import importlib.util
import inspect
import os
import sys
import time
from pathlib import Path
from pympler.asizeof import asizeof
from .interfaces import StreamingAlgorithm, BatchAlgorithm, PreprocessEdge
from .file_reading import CSVFile, MTXFile, FileProcessingStrategy, TEXTFile
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
        preprocess_path: Path | None,
        streaming_path: Path,
        batch_path: Path | None,
    ):
        self._dataset = dataset_path
        self._should_preprocess = preprocess_path is not None
        self._with_batch = batch_path is not None
        
        file_extension = self._dataset.suffix

        if file_extension =='.csv':
            self._file_reading: FileProcessingStrategy = CSVFile(self._dataset)
        elif file_extension == '.mtx':
            self._file_reading: FileProcessingStrategy = MTXFile(self._dataset)
        else:
            # dont ask 
            if self._should_preprocess:
                self._file_reading :FileProcessingStrategy = TEXTFile(self._dataset, self._preprocess.create_edge_from) # type:ignore
            else:
                self._file_reading :FileProcessingStrategy = TEXTFile(self._dataset)
        
        # time inverals are now saved using the perf_counter_ns for greater precision 
        self._calculation_time_per_edge = []
        self._preprocessing_time_per_edge = []
                
        # Saves the amount of stored memory in RAM (non-swapped) in MB by this runner process 
        # psutil implementation - will include everything including the sizes of the history and of the stream, batch object
        # stops recording when the streaming algorithm is done computing 
        # pympler implementation - is restricted to the object itself, is an approximation of its size
        self._memory_history = []
        self._number_of_processed_edges = 0
            
        self._streaming = get_class_instance_from(streaming_path)
        
        if self._should_preprocess:
            self._preprocess = get_class_instance_from(preprocess_path)  # type: ignore
            
        if self._with_batch:
            self._batch = get_class_instance_from(batch_path)  # type: ignore


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
    

    def validate_algorithm_signatures(self, row_data) -> tuple[bool, str]:
        stream_sig = inspect.signature(self._streaming.on_edge_calculate).parameters["edge"].annotation # type: ignore
        are_params_correct = type(row_data) == stream_sig
        message = ''
        if not are_params_correct:
            message += f"The given row data type: {type(row_data)} does not match the edge parameter {stream_sig} in the provided streaming algorithm.\n"

        if self._should_preprocess:
            preprocess_sig = inspect.signature(self._preprocess.create_edge_from).parameters['line'].annotation # type: ignore
            are_params_correct = are_params_correct or type(row_data)==preprocess_sig
            message += f"The given row data type: {type(row_data)} does not match the line parameter {preprocess_sig} in the provided preprocessing.\n"
        
        return are_params_correct, message
        
    
    def get_stream_results(self):
        return self._streaming.submit_results() # type: ignore
    
    def get_batch_results(self):
        return self._batch.submit_results() # type: ignore
   

    def get_jaccard_similarity(self):
        set_a = set(self.get_stream_results())
        set_b = set(self.get_batch_results())

        intersec = set_a.intersection(set_b)
        union = set_a.union(set_b)
        return float(len(intersec))/float(len(union))
    
    

    def get_streaming_accuracy(self):
        streaming_results = self._streaming.submit_results() # type: ignore
        batch_results = self._batch.submit_results() # type: ignore
        correct = 0
        for stream, batch in zip(streaming_results, batch_results):
            if stream[0] == batch[0]:
                correct +=1

        return correct/len(streaming_results)


    def validate_implementation(self):
        if not isinstance(self._streaming, StreamingAlgorithm): # type: ignore
            raise TypeError("Streaming algorithm is not implemeted right - cannot instantiate StreamingAlgorithm interface. Check if all methods have been supplied together with the right method name.")
        elif self._with_batch and ( not isinstance(self._batch, BatchAlgorithm)): # type:ignore
            raise TypeError("Batch algorithm is not implemeted right - cannot instantiate BatchAlgorithm interface. Check if all methods have been supplied together with the right method name.")
        elif self._should_preprocess and (not isinstance(self._preprocess, PreprocessEdge)): # type:ignore
            raise TypeError("Preprocessing algorithm is not implemeted right - cannot instantiate PreprocessEdge interface. Check if all methods have been supplied together with the right method name.")

    def run(self):
        # process = psutil.Process(os.getpid())
        

        # MB_ratio = 1/(1024*1024) 
        # self._memory_history.append([process.memory_info().rss*MB_ratio])
        self._memory_history.append(asizeof(self._streaming))
        
        with open(self._dataset, encoding="utf-8") as file:
            reader = self._file_reading.get_reader(file) # type: ignore
            self._file_reading.set_headers(reader)


            for row in reader: # type: ignore
                self._number_of_processed_edges += 1

                row = self._file_reading.process_row(row)

                if self._should_preprocess:
                    preprocess_start = time.perf_counter()
                   
                    preprocess_end = time.perf_counter()
                    preprocess_start = time.perf_counter_ns()
                    row = self._preprocess.create_edge_from(row) # type: ignore
                    preprocess_end = time.perf_counter_ns()
                    preprocess_duration = preprocess_end - preprocess_start
                    self._preprocessing_time_per_edge.append(
                        preprocess_duration
                    )

                property_start = time.perf_counter()
                self._streaming.on_edge_calculate(row)  # type: ignore
                property_end = time.perf_counter()
                property_start = time.perf_counter_ns()
                self._streaming.on_edge_calculate(row)  # type: ignore
                property_end = time.perf_counter_ns()


                property_calculation_duration = property_end - property_start
                self._calculation_time_per_edge.append(
                    property_calculation_duration 
                )

                # self._memory_history.append(process.memory_info().rss*MB_ratio)
                self._memory_history.append(asizeof(self._streaming))


            if self._with_batch:
                self._batch.calculate_property(self._file_reading.get_dataframe()) # type: ignore
                

        streaming_results = self._streaming.submit_results()  # type: ignore
        batch_results = self._batch.submit_results() if self._with_batch else None  # type: ignore

        return (
            streaming_results,
            batch_results,
            self._calculation_time_per_edge,
            self._preprocessing_time_per_edge,
        )
