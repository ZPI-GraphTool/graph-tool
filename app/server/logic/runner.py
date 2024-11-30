import importlib.util
import inspect
import os
import sys
import time
from pathlib import Path
from typing import Any

from pympler.asizeof import asizeof

from algorithms._config.interfaces import (
    BatchAlgorithm,
    PreprocessEdge,
    StreamingAlgorithm,
)
from app.server._config import (
    CONNECTION_PREPROCESSING_FUNCTION_FILE,
    CONNECTIONS_CSV_FILE,
)

from .file_reading import CSVFile, MTXFile, TEXTFile

ResultList = list[tuple[Any, int | float]]


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


def get_sampling_interval(total_count: int, sample_count: int) -> int:
    return total_count // sample_count


class Runner:
    def __init__(
        self,
        dataset_path: Path,
        preprocessing_path: Path | None,
        streaming_path: Path,
        batch_path: Path | None,
    ):
        self._dataset = dataset_path
        if self._dataset == CONNECTIONS_CSV_FILE and preprocessing_path is None:
            preprocessing_path = CONNECTION_PREPROCESSING_FUNCTION_FILE
        self._with_preprocessing = preprocessing_path is not None
        self._with_batch = batch_path is not None

        file_extension = self._dataset.suffix

        if file_extension == ".csv":
            self._file_reading = CSVFile(self._dataset)
        elif file_extension == ".mtx":
            self._file_reading = MTXFile(self._dataset)
        else:
            # dont ask
            if self._with_preprocessing:
                self._file_reading = TEXTFile(
                    self._dataset, self._preprocessing.create_edge_from
                )
            else:
                self._file_reading = TEXTFile(self._dataset)

        # time inverals are now saved using the perf_counter_ns for greater precision
        self._calculation_time_per_edge = []
        self._preprocessing_time_per_edge = []

        with open(self._dataset, encoding="utf-8") as file:
            reader: Any = self._file_reading.get_reader(file)
            self._file_reading.set_headers(reader)
            self._row_count = sum(1 for _ in reader)

        # Saves the amount of stored memory in RAM (non-swapped) in MB by this runner process
        # psutil implementation - will include everything including the sizes of the history and of the stream, batch object
        # stops recording when the streaming algorithm is done computing
        # pympler implementation - is restricted to the object itself, is an approximation of its size
        self._memory_usage = []
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
    def edge_count(self) -> int:
        return self._row_count

    @property
    def dataset_size(self) -> int:
        return self._dataset.stat().st_size

    @property
    def calculation_time_per_edge(self) -> list[int]:
        return self._calculation_time_per_edge

    @property
    def preprocessing_time_per_edge(self) -> list[int]:
        return self._preprocessing_time_per_edge

    @property
    def memory_usage(self) -> list[int]:
        return self._memory_usage

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

    def get_stream_results(self) -> ResultList:
        return self._streaming.submit_results()

    def get_batch_results(self) -> ResultList:
        return self._batch.submit_results() if self._with_batch else []

    def get_parameterized_results(
        self, orderDescending: bool, cardinality: int
    ) -> tuple[ResultList, ResultList]:
        streaming_results = sorted(self.get_stream_results(), reverse=orderDescending)
        batch_results = sorted(self.get_batch_results(), reverse=orderDescending)
        return streaming_results[:cardinality], batch_results[:cardinality]

    def get_jaccard_similarity(
        self, orderDescending: bool, cardinality: int = 10
    ) -> float:
        streaming_results, batch_results = self.get_parameterized_results(
            orderDescending, cardinality
        )

        streaming_results = [node for node, val in streaming_results]
        batch_results = [node for node, val in batch_results]

        set_a = set(streaming_results)
        set_b = set(batch_results)

        intersection = set_a.intersection(set_b)
        union = set_a.union(set_b)

        return len(intersection) / len(union)

    def get_streaming_accuracy(
        self, orderDescending: bool = False, cardinality: int = 10
    ) -> float:
        streaming_results, batch_results = self.get_parameterized_results(
            orderDescending, cardinality
        )
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

    def run_experiment(self, sample_count: int = 100) -> None:
        sampling_interval = get_sampling_interval(self._row_count, sample_count)
        # process = psutil.Process(os.getpid())

        # MB_ratio = 1/(1024*1024)
        # self._memory_usage.append([process.memory_info().rss*MB_ratio])

        with open(self._dataset, encoding="utf-8") as file:
            reader = self._file_reading.get_reader(file)

            for row in reader:  # type: ignore
                row: Any = self._file_reading.process_row(row)

                if self._with_preprocessing:
                    preprocessing_start = time.perf_counter_ns()
                    row = self._preprocessing.create_edge_from(row)
                    preprocessing_end = time.perf_counter_ns()
                    preprocessing_duration = preprocessing_end - preprocessing_start
                    self._preprocessing_time_per_edge.append(preprocessing_duration)
               
                property_start = time.perf_counter_ns()
                
                self._streaming.on_edge_calculate(row)  # type: ignore
                
                property_end = time.perf_counter_ns()
                calculation_duration = property_end - property_start
                self._calculation_time_per_edge.append(calculation_duration)

                if self._processed_edge_count % sampling_interval == 0:
                    self._memory_usage.append(
                        (self._processed_edge_count, asizeof(self._streaming))
                    )
                self._processed_edge_count += 1

            if self._with_batch:
                self._batch.calculate_property(self._file_reading.get_dataframe())  # type: ignore
