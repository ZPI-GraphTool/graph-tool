import importlib.util
import inspect
import os
import sys
from pathlib import Path

from demos import (
    CONNECTIONS_CSV_FILE,
    DEGREE_CENTRALITY_BATCH_ALGORITHM_FILE,
    DEGREE_CENTRALITY_STREAM_ALGORITHM_FILE,
)
from shiny import reactive, render, ui

from .logic import Runner
from .logic.actions import AlgorithmType, edit_algorithm, save_results


def get_class_name_from(file_path: Path) -> str | None:
    module_name = os.path.basename(file_path)

    spec = importlib.util.spec_from_file_location(str(file_path), file_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore

    for name_local in dir(module):
        if inspect.isclass(getattr(module, name_local)):
            return name_local
    return None


def get_algorithm_names(directory: str) -> dict[str, str]:
    algorithm_names: dict[str, str] = {}
    algorithms_directory = Path(__file__).parents[1] / "algorithms" / directory
    for i, algorithm_file in enumerate(algorithms_directory.glob("*.py")):
        algorithm_name = get_class_name_from(algorithm_file)
        if algorithm_name is not None:
            algorithm_names.update({str(algorithm_file): algorithm_name})
    return algorithm_names


def server(input, output, session):
    @render.ui
    @reactive.event(input.refresh_preprocess_list, ignore_none=False)
    def render_preprocess_selectize():
        return (
            ui.input_selectize(
                "select_preprocess",
                "",
                {
                    "": {"0": "New function"},
                    "Existing": get_algorithm_names("preprocess"),
                },
                selected="0",
            ),
        )

    @render.ui
    @reactive.event(input.refresh_algorithm_list, ignore_none=False)
    def render_algorithm_selectize():
        return (
            ui.input_selectize(
                "select_algorithm",
                "",
                {
                    "Provided by me": {
                        "0": "New batch algorithm",
                        "1": "New streaming algorithm",
                    },
                    "Batch": get_algorithm_names("batch"),
                    "Streaming": get_algorithm_names("streaming"),
                    "Presupplied": {
                        "2": "Degree centrality batch",
                        "3": "Degree centrality stream",
                    },
                },
                selected="2",
            ),
        )

    @reactive.effect
    @reactive.event(input.edit_preprocessing)
    def _():
        edit_algorithm(AlgorithmType.PREPROCESS)

    @reactive.effect
    @reactive.event(input.edit_algorithm)
    def _():
        edit_algorithm(input.select_algorithm())

    @reactive.calc
    def parse_file() -> Path:
        dataset_path: Path
        match input.select_dataset():
            case "0":
                dataset_path = input.dataset_path()
            case "1":
                dataset_path = CONNECTIONS_CSV_FILE
        return dataset_path

    @reactive.calc
    def _() -> Path:
        algorithm_path: Path
        match input.select_algorithm():
            case "2":
                algorithm_path = DEGREE_CENTRALITY_BATCH_ALGORITHM_FILE
            case "3":
                algorithm_path = DEGREE_CENTRALITY_STREAM_ALGORITHM_FILE
        return algorithm_path

    @output
    @render.ui
    @reactive.event(input.run_experiment)
    async def compute():
        data = parse_file()

        runner = Runner(
            data,
            streaming_path=DEGREE_CENTRALITY_STREAM_ALGORITHM_FILE,
            batch_path=DEGREE_CENTRALITY_BATCH_ALGORITHM_FILE,
        )
        stream, batch, _, _ = runner.run()
        print(batch)

    @reactive.effect
    @reactive.event(input.save_results)
    def _():
        save_results()

    # @render.plot
    # def plot():
    #     some_dist = pd.Series([1, 2, 3, 4, 5])

    #     fig, ax = plt.subplots()
    #     ax.hist(some_dist)
    #     plt.savefig("plot.png")
    #     return fig
