from shiny import ui

from .batch import batch
from .dataset import dataset
from .preprocessing import preprocessing
from .streaming import streaming

sidebar = ui.sidebar(
    ui.input_dark_mode(id="mode", mode="light"),
    *dataset(),
    *preprocessing(),
    *streaming(),
    *batch(),
    ui.input_action_button("run_experiment", "Run experiment"),
    ui.input_action_button("save_results", "Save results"),
    width=320,
    title=ui.input_text("experiment_name", label="Experiment name"),
)
