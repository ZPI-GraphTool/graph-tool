import traceback
from pathlib import Path
from typing import Any

from shiny import Inputs, reactive

from app.server._config import CONNECTIONS_CSV_FILE
from app.server.logic import Runner


class MissingPathError(ValueError):
    def __init__(self, object_name: str) -> None:
        super().__init__(
            f"No {object_name} path was selected. Please provide a valid path to the {object_name}."
        )


def select_dataset(option: str, path: list[dict[str, str]]) -> Path:
    match option:
        case "0":
            if path is None:
                raise MissingPathError("dataset")
            dataset_path = Path(path[0]["datapath"])
        case "1":
            dataset_path = CONNECTIONS_CSV_FILE
    return dataset_path


def get_paths(input: Inputs) -> tuple[Any, ...]:
    dataset_path: Path = select_dataset(input.select_dataset(), input.dataset_path())
    preprocess_path: Path | None = (
        input.select_preprocessing() if input.with_preprocessing() else None
    )
    streaming_path: Path = input.select_streaming()
    batch_path: Path | None = input.select_batch() if input.with_batch() else None

    return dataset_path, preprocess_path, streaming_path, batch_path


def server_run_experiment(
    input: Inputs, results: dict[str, reactive.Value], errors: reactive.Value
) -> None:
    @reactive.effect
    @reactive.event(input.run_experiment)
    def _():
        try:
            dataset_path, preprocess_path, streaming_path, batch_path = get_paths(input)
            runner = Runner(
                dataset_path=dataset_path,
                preprocessing_path=preprocess_path,
                streaming_path=streaming_path,
                batch_path=batch_path,
            )
            runner.validate_implementation()
            runner.run_experiment()
        except TypeError as type_error:
            errors.set(type_error)
        except MissingPathError as missing_path_error:
            errors.set(missing_path_error)
        except UnicodeDecodeError:
            errors.set(
                "The dataset you provided is not in a UTF-8-compatible encoding."
            )
        except Exception:
            errors.set(traceback.format_exc())
        else:
            results["streaming"].set(runner.get_stream_results())
            results["batch"].set(runner.get_batch_results())
            results["calculation_time"].set(runner.calculation_time_per_edge)
            results["memory"].set(runner.memory_history)
            results["jaccard_similarity"].set(runner.get_jaccard_similarity())
            results["streaming_accuracy"].set(runner.get_streaming_accuracy())
