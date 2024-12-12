import os

from shiny import Inputs, Outputs, Session, reactive, ui

__all__ = ["server", "kill_python"]

from .reactives import (
    server_edit,
    server_results,
    server_run_experiment,
    server_selectize,
)

error = reactive.value()

run_paths = {
    "dataset_path": reactive.value(),
    "preprocessing_path": reactive.value(),
    "streaming_path": reactive.value(),
    "batch_path": reactive.value(),
}

results = {
    "runner": reactive.value(),
    "streaming_results": reactive.value(),
    "batch_results": reactive.value(),
    "calculation_time": reactive.value(),
    "memory_usage": reactive.value(),
    "jaccard_similarity": reactive.value(),
    "streaming_accuracy": reactive.value(),
}


def kill_python():
    os.kill(os.getpid(), 9)


def server(input: Inputs, output: Outputs, session: Session):
    server_selectize(input)
    server_edit(input, error)
    server_run_experiment(input, run_paths, results, error)
    server_results(input, run_paths, results, error)

    @reactive.effect
    @reactive.event(error)
    def show_error_modal():
        error_rand, error_message = error.get()
        modal = ui.modal(error_message, title="Error", easy_close=True, size="l")
        ui.modal_show(modal)

    @reactive.effect
    @reactive.event(input.close_app)
    def close_app():
        kill_python()
