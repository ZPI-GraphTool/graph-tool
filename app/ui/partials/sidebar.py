import faicons as fa
from shiny import ui

sidebar = ui.sidebar(
    ui.input_selectize(
        "select_dataset",
        "Dataset",
        {
            "Provided by me": {"0": "Custom dataset"},
            "Presupplied": {"1": "Public transport connections"},
        },
        selected="1",
    ),
    ui.panel_conditional(
        "input.select_dataset == 0",
        ui.input_file("dataset_path", "Path to dataset"),
        ui.input_switch("preprocess_data", "Preprocess data", False),
    ),
    ui.panel_conditional(
        "input.preprocess_data == true",
        ui.row(
            ui.column(8, "Preprocessing function", class_="selectize-label"),
            ui.column(
                3,
                ui.input_action_button(
                    "refresh_preprocess_list",
                    label="",
                    icon=fa.icon_svg("rotate"),
                    class_="refresh-button",
                ),
            ),
            class_="selectize-row",
        ),
        ui.output_ui("render_preprocess_selectize"),
        ui.panel_conditional(
            "input.select_preprocess== 0",
            ui.input_action_button("edit_preprocessing", "Edit preprocessing function"),
        ),
    ),
    ui.row(
        ui.column(4, "Algorithms", class_="selectize-label"),
        ui.column(
            3,
            ui.input_action_button(
                "refresh_algorithm_list",
                label="",
                icon=fa.icon_svg("rotate"),
                class_="refresh-button",
            ),
        ),
        class_="selectize-row",
    ),
    ui.output_ui("render_algorithm_selectize"),
    ui.panel_conditional(
        "input.select_algorithm < 2",
        ui.input_action_button("edit_algorithm", "Edit algorithm"),
    ),
    ui.input_action_button("run_experiment", "Run experiment"),
    width=320,
    title=ui.input_text("experiment_title", label=None, placeholder="Experiment title"),
)
