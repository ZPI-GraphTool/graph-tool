import faicons as fa
from shiny import ui

from .batch import batch
from .dataset import dataset
from .preprocessing import preprocessing
from .streaming import streaming

sidebar = ui.sidebar(
    ui.input_dark_mode(id="mode", mode="light"),
    ui.input_action_button(
        "close_app", "Close", icon=fa.icon_svg("xmark"), class_="btn-outline-danger"
    ),
    *dataset(),
    *preprocessing(),
    *streaming(),
    *batch(),
    ui.tags.div(class_="flex-divider"),
    ui.output_ui("save_results_button"),
    ui.input_task_button(
        "run_experiment",
        "Run experiment",
        icon=fa.icon_svg("play"),
        label_busy="Running...",
        class_="btn-outline-primary",
    ),
    width=320,
    title=ui.input_text("experiment_name", label="Experiment name"),
)
