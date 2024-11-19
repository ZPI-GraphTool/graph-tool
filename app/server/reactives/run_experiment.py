import traceback
from pathlib import Path

from demos import CONNECTIONS_CSV_FILE
from server.logic import Runner
from shiny import reactive

results = reactive.value()


def select_dataset(option: str, path: Path) -> Path:
    match option:
        case "0":
            dataset_path = Path(path)
        case "1":
            dataset_path = CONNECTIONS_CSV_FILE
    return dataset_path


def get_paths(input):
    dataset_path = select_dataset(input.select_dataset(), input.dataset_path())
    preprocess_path = (
        input.select_preprocessing() if input.with_preprocessing() else None
    )
    streaming_path = input.select_streaming()
    batch_path = input.select_batch() if input.with_batch() else None

    return dataset_path, preprocess_path, streaming_path, batch_path


def server_run_experiment(
    input, results: dict[str, reactive.value], errors: reactive.value
):
    @reactive.effect
    @reactive.event(input.run_experiment)
    def run_experiment():
        dataset_path, preprocess_path, streaming_path, batch_path = get_paths(input)

        try:
            runner = Runner(
                dataset_path=dataset_path,
                preprocessing_path=preprocess_path,
                streaming_path=streaming_path,
                batch_path=batch_path,
            )
            runner.validate_implementation()
            runner.run()
        except TypeError as type_error:
            errors.set(type_error)
        except Exception:
            errors.set(traceback.format_exc())

        results["streaming"].set(runner.get_stream_results())
        # results["batch"].set(runner.get_batch_results())
        # results["preprocessing_time"].set(runner.preprocessing_time_per_edge)
        results["calculation_time"].set(runner.calculation_time_per_edge)
        results["memory"].set(runner.memory_history)
