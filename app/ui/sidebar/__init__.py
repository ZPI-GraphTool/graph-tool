from shiny import ui

from .partials import batch, dataset, preprocessing, streaming

sidebar = ui.sidebar(
    *dataset(),
    *preprocessing(),
    *streaming(),
    *batch(),
    ui.input_action_button("run_experiment", "Run experiment"),
    ui.input_action_button("save_results", "Save results"),
    width=320,
    title=ui.input_text("experiment_name", label=None, placeholder="Experiment name"),
)
