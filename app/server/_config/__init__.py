import importlib.util
import inspect
import os
import shelve
import sys
from enum import StrEnum
from pathlib import Path

from algorithms._config.interfaces import (
    BatchAlgorithm,
    PreprocessEdge,
    StreamingAlgorithm,
)

EXECUTABLE = sys.executable.split("\\")[-1]
parent_index = 3 if EXECUTABLE == "python.exe" else 4

PROJECT_DIRECTORY = Path(__file__).resolve().parents[parent_index]


DEMOS_DIRECTORY = PROJECT_DIRECTORY / "demos"

CONNECTIONS_CSV_FILE = DEMOS_DIRECTORY / "connections.csv"
CONNECTION_PREPROCESSING_FUNCTION_FILE = DEMOS_DIRECTORY / "connection_preprocessing.py"
DEGREE_CENTRALITY_BATCH_ALGORITHM_FILE = DEMOS_DIRECTORY / "degree_centrality_batch.py"
DEGREE_CENTRALITY_STREAM_ACCURATE_ALGORITHM_FILE = (
    DEMOS_DIRECTORY / "degree_centrality_accurate_stream.py"
)
DEGREE_CENTRALITY_STREAM_APPROXIMATE_ALGORITHM_FILE = (
    DEMOS_DIRECTORY / "degree_centrality_approximate_stream.py"
)
MISRA_GRIES_STREAM_ALGORITHM_FILE = DEMOS_DIRECTORY / "stream_misra_gries.py"
PREDEFINED_ALGORITHMS = [
    CONNECTION_PREPROCESSING_FUNCTION_FILE,
    DEGREE_CENTRALITY_BATCH_ALGORITHM_FILE,
    DEGREE_CENTRALITY_STREAM_ACCURATE_ALGORITHM_FILE,
    DEGREE_CENTRALITY_STREAM_APPROXIMATE_ALGORITHM_FILE,
    MISRA_GRIES_STREAM_ALGORITHM_FILE,
]


ALGORITHMS_DIRECTORY = PROJECT_DIRECTORY / "algorithms"
ALGORITHM_TEMPLATES_DIRECTORY = ALGORITHMS_DIRECTORY / "_config" / "templates"

EXPERIMENTS_DIRECTORY = PROJECT_DIRECTORY / "experiments"


class AlgorithmType(StrEnum):
    PREPROCESSING = "preprocessing"
    BATCH = "batch"
    STREAMING = "streaming"


class AlgorithmTypeSpecification:
    @classmethod
    def new_file(cls, algorithm_type: AlgorithmType) -> str:
        prefix: str = ""
        match algorithm_type:
            case AlgorithmType.STREAMING:
                prefix = "streaming_algorithm"
            case AlgorithmType.BATCH:
                prefix = "batch_algorithm"
            case AlgorithmType.PREPROCESSING:
                prefix = "preprocessing_function"
        # this caches how many files of each type have been created so far
        # so that we know what number to name the new file of a given type
        with shelve.open(ALGORITHMS_DIRECTORY / "counter") as counter:
            key = f"{algorithm_type}_counter"
            if key not in counter:
                counter[key] = 0
            file_name = f"{prefix}_{counter[key]}.py"
            counter[key] += 1
        return file_name

    @classmethod
    def paths(cls, algorithm_type: AlgorithmType) -> tuple[Path, Path]:
        template_path = ALGORITHM_TEMPLATES_DIRECTORY / f"template_{algorithm_type}.py"
        destination_directory = ALGORITHMS_DIRECTORY / algorithm_type
        destination_directory.mkdir(parents=True, exist_ok=True)
        destination = destination_directory / cls.new_file(algorithm_type)
        return template_path, destination

    @classmethod
    def get_type_hint_message(
        cls, algorithm_type: AlgorithmType, dataset_type: str
    ) -> str:
        message = ""

        match algorithm_type, dataset_type[1:]:
            case AlgorithmType.BATCH, "csv":
                message = "\t# The dataframe's columns are the headers of the supplied .csv file.\n"
            case AlgorithmType.BATCH, "mtx":
                message = "\t# The dataframe's columns are: 0 - source node, 1 - destination node, 2 - weight of the edge (equal 1.0 for unweighted graphs).\n"
            case AlgorithmType.BATCH, _:
                message = "\t# The dataframe only has one column 0 unless a specified preprocessing method has been supplied which converts the string line into an object (like a tuple).\n\t# In that case it follows how pandas creates DataFrames based on a list of those objects\n"
            case AlgorithmType.PREPROCESSING, "csv":
                message = "\t# The edge is a dictionary. Its keys are the headers of the supplied .csv file.\n"
            case AlgorithmType.PREPROCESSING, "mtx":
                message = "\t# The given edge is a tuple: 0 - source node, 1 - destination node, 2 - weight of the edge  (equal 1.0 for unweighted graphs) \n"
            case AlgorithmType.PREPROCESSING, _:
                message = "\t# The edge is an unedited string equivalent to one line from the file.\n"
            case _, "csv":
                message = "\t# The edge is a dictionary (keys are the headers of the .csv file)\n\t# or a type specified by a preprocessing function.\n"
            case _, "mtx":
                message = "\t# The given edge is a tuple: 0 - source node, 1 - destination node, 2 - weight of the edge  (equal 1.0 for unweighted graphs) \n\t# or a type specified by a preprocessing function\n"
            case _, _:
                message = "\t# The edge is a string unless a specified preprocessing method has been supplied.\n\t# In the latter case the format of the edge matches the return of the preprocessing method.\n"

        return message


def get_class_name_from(file_path: str | Path) -> str | None:
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
            return name_local
