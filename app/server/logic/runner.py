import importlib.util
import inspect
import os
import sys
import time
from pathlib import Path
from typing import Any

from pympler.asizeof import asizeof

from .file_reading import CSVFile, FileProcessingStrategy, MTXFile, TEXTFile
from .interfaces import BatchAlgorithm, PreprocessEdge, StreamingAlgorithm, numeric


def get_class_instance_from(
    file_path: Path,
) -> BatchAlgorithm | PreprocessEdge | StreamingAlgorithm | None:
    module_name = os.path.basename(file_path)

    spec = importlib.util.spec_from_file_location(str(file_path), file_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore

    for name_local in dir(module):
        mysterious_thing = getattr(module, name_local)
        if not inspect.isclass(mysterious_thing):
            continue
        MysteriousClass = mysterious_thing
        if not inspect.isabstract(MysteriousClass) and issubclass(
            MysteriousClass, (BatchAlgorithm, PreprocessEdge, StreamingAlgorithm)
        ):
            return MysteriousClass()


class Runner:
    def __init__(
        self,
        dataset_path: Path,
        preprocessing_path: Path | None,
        streaming_path: Path,
        batch_path: Path | None,
    ):
        self._dataset = dataset_path
        self._with_preprocessing = preprocessing_path is not None
        self._with_batch = batch_path is not None

        file_extension = self._dataset.suffix

        if file_extension == ".csv":
            self._file_reading: FileProcessingStrategy = CSVFile(self._dataset)
        elif file_extension == ".mtx":
            self._file_reading: FileProcessingStrategy = MTXFile(self._dataset)
        else:
            # dont ask
            if self._with_preprocessing:
                self._file_reading: FileProcessingStrategy = TEXTFile(
                    self._dataset, self._preprocessing.create_edge_from
                )
            else:
                self._file_reading: FileProcessingStrategy = TEXTFile(self._dataset)

        # time inverals are now saved using the perf_counter_ns for greater precision
        self._calculation_time_per_edge = []
        self._preprocessing_time_per_edge = []

        # Saves the amount of stored memory in RAM (non-swapped) in MB by this runner process
        # psutil implementation - will include everything including the sizes of the history and of the stream, batch object
        # stops recording when the streaming algorithm is done computing
        # pympler implementation - is restricted to the object itself, is an approximation of its size
        self._memory_history = []
        self._processed_edge_count = 0

        if self._with_preprocessing:
            self._preprocessing: PreprocessEdge = get_class_instance_from(
                preprocessing_path  # type: ignore
            )

        self._streaming: StreamingAlgorithm = get_class_instance_from(streaming_path)  # type: ignore

        if self._with_batch:
            self._batch: BatchAlgorithm = get_class_instance_from(batch_path)  # type: ignore

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
        stream_signature = (
            inspect.signature(self._streaming.on_edge_calculate)
            .parameters["edge"]
            .annotation
        )
        are_params_correct = type(row_data) is stream_signature
        message = ""
        if not are_params_correct:
            message += f"The given row data type: {type(row_data)} does not match the edge parameter {stream_signature} in the provided streaming algorithm.\n"

        if self._with_preprocessing:
            preprocessing_signature = (
                inspect.signature(self._preprocessing.create_edge_from)
                .parameters["line"]
                .annotation
            )
            are_params_correct = (
                are_params_correct or type(row_data) is preprocessing_signature
            )
            message += f"The given row data type: {type(row_data)} does not match the line parameter {preprocessing_signature} in the provided preprocessing.\n"

        return are_params_correct, message

    def get_stream_results(self) -> list[tuple[Any, numeric]]:
        return self._streaming.submit_results()

    def get_batch_results(self) -> list[tuple[Any, numeric]]:
        return self._batch.submit_results() if self._with_batch else []

    def get_jaccard_similarity(self) -> float:
        set_a = set(self.get_stream_results())
        set_b = set(self.get_batch_results())

        intersection = set_a.intersection(set_b)
        union = set_a.union(set_b)
        return float(len(intersection)) / float(len(union))

    def get_streaming_accuracy(self) -> float:
        streaming_results = self.get_stream_results()
        batch_results = self.get_batch_results()
        correct = 0
        for stream, batch in zip(streaming_results, batch_results):
            if stream[0] == batch[0]:
                correct += 1

        return correct / len(streaming_results)

    def validate_implementation(self) -> None:
        if not isinstance(self._streaming, StreamingAlgorithm):
            raise TypeError(
                "Streaming algorithm is not implemeted right - cannot instantiate StreamingAlgorithm interface. Check if all methods have been supplied together with the right method name."
            )
        elif self._with_batch and (not isinstance(self._batch, BatchAlgorithm)):
            raise TypeError(
                "Batch algorithm is not implemeted right - cannot instantiate BatchAlgorithm interface. Check if all methods have been supplied together with the right method name."
            )
        elif self._with_preprocessing and (
            not isinstance(self._preprocessing, PreprocessEdge)
        ):
            raise TypeError(
                "Preprocessing algorithm is not implemeted right - cannot instantiate PreprocessEdge interface. Check if all methods have been supplied together with the right method name."
            )

    def run_experiment(self):
        # process = psutil.Process(os.getpid())

        # MB_ratio = 1/(1024*1024)
        # self._memory_history.append([process.memory_info().rss*MB_ratio])
        self._memory_history.append(asizeof(self._streaming))

        with open(self._dataset, encoding="utf-8") as file:
            reader = self._file_reading.get_reader(file)
            self._file_reading.set_headers(reader)

            for row in reader:  # type: ignore
                row = self._file_reading.process_row(row)
                self._processed_edge_count += 1

                if self._with_preprocessing:
                    preprocessing_start = time.perf_counter_ns()
                    row = self._preprocessing.create_edge_from(row)
                    preprocessing_end = time.perf_counter_ns()
                    preprocessing_duration = preprocessing_end - preprocessing_start
                    self._preprocessing_time_per_edge.append(preprocessing_duration)

                property_start = time.perf_counter_ns()
                self._streaming.on_edge_calculate(row, "start_stop", "end_stop")  # type: ignore
                property_end = time.perf_counter_ns()
                calculation_duration = property_end - property_start
                self._calculation_time_per_edge.append(calculation_duration)

                # self._memory_history.append(process.memory_info().rss*MB_ratio)
                self._memory_history.append(asizeof(self._streaming))

            if self._with_batch:
                self._batch.calculate_property(self._file_reading.get_dataframe())  # type: ignore
