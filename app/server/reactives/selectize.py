import importlib.util
import inspect
import os
import sys
from pathlib import Path

from shiny import Inputs, reactive, render, ui

from algorithms._config.interfaces import (
    BatchAlgorithm,
    PreprocessEdge,
    StreamingAlgorithm,
)
from app.server._config import (
    ALGORITHMS_DIRECTORY,
    CONNECTION_PREPROCESSING_FUNCTION_FILE,
    DEGREE_CENTRALITY_BATCH_ALGORITHM_FILE,
    DEGREE_CENTRALITY_STREAM_ACCURATE_ALGORITHM_FILE,
    DEGREE_CENTRALITY_STREAM_APPROXIMATE_ALGORITHM_FILE,
    MISRA_GRIES_STREAM_ALGORITHM_FILE,
    AlgorithmType,
)


def get_class_name_from(file_path: Path) -> str | None:
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


def get_algorithms(type: AlgorithmType) -> dict[str, str]:
    algorithms: dict[str, str] = {}
    algorithms_type_directory = ALGORITHMS_DIRECTORY / type
    for algorithm_file in algorithms_type_directory.glob("*.py"):
        algorithm_name = get_class_name_from(algorithm_file)
        if algorithm_name is not None:
            algorithms.update({str(algorithm_file): algorithm_name})
    return algorithms


def server_selectize(input: Inputs) -> None:
    @render.ui
    @reactive.event(input.refresh_preprocessing_list, ignore_none=False)
    def preprocessing_selectize():
        return (
            ui.input_selectize(
                "select_preprocessing",
                "",
                {
                    "": {"New": "New function"},
                    "Existing": get_algorithms(AlgorithmType.PREPROCESSING),
                    "Presupplied": {
                        str(
                            CONNECTION_PREPROCESSING_FUNCTION_FILE
                        ): "Connection preprocessing",
                    },
                },
                selected="New",
            ),
        )

    @render.ui
    @reactive.event(input.refresh_streaming_list, ignore_none=False)
    def streaming_selectize():
        return (
            ui.input_selectize(
                "select_streaming",
                "",
                {
                    "": {"New": "New algorithm"},
                    "Existing": get_algorithms(AlgorithmType.STREAMING),
                    "Presupplied": {
                        str(
                            DEGREE_CENTRALITY_STREAM_ACCURATE_ALGORITHM_FILE
                        ): "Degree centrality stream accurate",
                        str(
                            DEGREE_CENTRALITY_STREAM_APPROXIMATE_ALGORITHM_FILE
                        ): "Degree centrality stream approximate",
                        str(MISRA_GRIES_STREAM_ALGORITHM_FILE): "Misra-Gries stream",
                    },
                },
                selected=str(DEGREE_CENTRALITY_STREAM_ACCURATE_ALGORITHM_FILE),
            ),
        )

    @render.ui
    @reactive.event(input.refresh_batch_list, ignore_none=False)
    def batch_selectize():
        return (
            ui.input_selectize(
                "select_batch",
                "",
                {
                    "": {"New": "New algorithm"},
                    "Existing": get_algorithms(AlgorithmType.BATCH),
                    "Presupplied": {
                        str(
                            DEGREE_CENTRALITY_BATCH_ALGORITHM_FILE
                        ): "Degree centrality batch",
                    },
                },
                selected=str(DEGREE_CENTRALITY_BATCH_ALGORITHM_FILE),
            ),
        )
