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
        if inspect.isclass(getattr(module, name_local)):
            MysteriousClass = getattr(module, name_local)

            # checks if the mystery class is not abstract
            if not inspect.isabstract(MysteriousClass):
                return MysteriousClass()


class Runner:
    def __init__(
        self,
        dataset_path: Path = Path(""),
        preprocess_path: Path = Path(""),
        streaming_path: Path = Path(""),
        batch_path: Path = Path(""),
    ):
        self._should_preprocess = not preprocess_path
        self._dataset = dataset_path

        if self._should_preprocess:
            self._preprocess = get_class_instance_from(preprocess_path)

        self._batch = get_class_instance_from(batch_path)
        self._stream = get_class_instance_from(streaming_path)

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
                    preprocess_start = time.time()
                    # processssss
                    preprocess_end = time.time()
                    preprocess_duration = preprocess_end - preprocess_start
                    self._avg_preprocessing_time_per_edge.append(
                        preprocess_duration / self._number_of_processed_edges
                    )

                property_start = time.time()
                self._stream.on_edge_calculate(row)  # type: ignore
                property_end = time.time()
                property_calculation_duration = property_end - property_start
                self._avg_property_time_per_edge.append(
                    property_calculation_duration / self._number_of_processed_edges
                )

            if os.path.basename(self._dataset).endswith(".csv"):
                self._batch.calculate_property(pd.read_csv(self._dataset))  # type: ignore

            elif os.path.basename(self._dataset).endswith(".mtx"):
                # TODO: convert mtx to dataframe
                pass

            else:
                # TODO: how to make it possible to batch process when the best we got is some text file
                # batch processing atm requires a pandas DataFrame
                pass

        return (
            self._stream.submit_results(),  # type: ignore
            self._batch.submit_results(),  # type: ignore
            self._avg_property_time_per_edge,
            self._avg_preprocessing_time_per_edge,
        )
