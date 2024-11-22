import os

from shiny import Inputs, Outputs, Session, reactive, ui

from .reactives import (
    server_edit,
    server_results,
    server_run_experiment,
    server_selectize,
)

errors = reactive.value()

streaming_results = reactive.value()
batch_results = reactive.value()
calculation_time = reactive.value()
memory_history = reactive.value()

results = {
    "streaming": streaming_results,
    "batch": batch_results,
    "calculation_time": calculation_time,
    "memory": memory_history,
}


def server(input: Inputs, output: Outputs, session: Session):
    server_selectize(input)
    server_edit(input)
    server_run_experiment(input, results, errors)
    server_results(input, results)

    @reactive.effect
    @reactive.event(errors)
    def show_error_modal():
        modal = ui.modal(str(errors.get()), title="Error", easy_close=True)
        ui.modal_show(modal)

    @reactive.effect
    @reactive.event(input.close_app)
    def close_app():
        os.kill(os.getpid(), 9)
