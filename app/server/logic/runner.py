import csv
import importlib.util
import inspect
import os
import sys
import time
from pathlib import Path

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

        if self._should_preprocess:
            self._preprocess = get_class_instance_from(preprocess_path)  # type: ignore

        self._streaming = get_class_instance_from(streaming_path)

        if self._with_batch:
            self._batch = get_class_instance_from(batch_path)  # type: ignore

        self._avg_property_time_per_edge = []
        self._avg_preprocessing_time_per_edge = []
        self._number_of_processed_edges = 0

    def run(self):
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
        with open(self._dataset, encoding="utf-8") as file:
            reader = csv.DictReader(
                file, fieldnames=columns
            )  # , is the default delimiter
            next(reader, None)

            for row in reader:
                self._number_of_processed_edges += 1

                if self._should_preprocess:
                    preprocess_start = time.perf_counter()
                    # processssss
                    preprocess_end = time.perf_counter()
                    preprocess_duration = preprocess_end - preprocess_start
                    self._avg_preprocessing_time_per_edge.append(
                        preprocess_duration / self._number_of_processed_edges
                    )

                property_start = time.perf_counter()
                self._streaming.on_edge_calculate(row)  # type: ignore
                property_end = time.perf_counter()
                property_calculation_duration = property_end - property_start
                self._avg_property_time_per_edge.append(
                    property_calculation_duration / self._number_of_processed_edges
                )

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

        streaming_results = self._streaming.submit_results()  # type: ignore
        batch_results = self._batch.submit_results() if self._with_batch else None  # type: ignore

        return (
            streaming_results,
            batch_results,
            self._avg_property_time_per_edge,
            self._avg_preprocessing_time_per_edge,
        )
