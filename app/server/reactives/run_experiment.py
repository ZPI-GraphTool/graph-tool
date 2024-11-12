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


def server_run_experiment(input):
    @reactive.effect
    @reactive.event(input.run_experiment)
    def run_experiment():
        dataset_path = select_dataset(input.select_dataset(), input.dataset_path())  # type: ignore
        preprocess_path = (
            input.select_preprocessing() if input.with_preprocessing() else None
        )
        streaming_path = input.select_streaming()
        batch_path = input.select_batch() if input.with_batch() else None

        runner = Runner(
            dataset_path=dataset_path,
            preprocess_path=preprocess_path,
            streaming_path=streaming_path,
            batch_path=batch_path,
        )
        results.set(runner.run())  # type: ignore
