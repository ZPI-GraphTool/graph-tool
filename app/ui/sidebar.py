from shiny import ui

sidebar = ui.sidebar(
    ui.input_selectize(
        "select_dataset",
        "Select dataset",
        {
            "Supplied": {"1": "Dataset 1", "2": "Dataset 2"},
            "Provided by me": {"0": "Provided by me"},
        },
    ),
    ui.panel_conditional(
        "input.select_dataset == 0",
        ui.input_file("dataset_path", "Provide path to dataset"),
    ),
    ui.panel_conditional(
        "input.select_dataset == 0",
        ui.input_switch("preprocess_data", "Preprocess data", False),
    ),
    ui.panel_conditional(
        "input.preprocess_data == true",
        ui.input_action_button("edit_preprocessing", "Edit preprocessing function"),
    ),
    ui.input_select(
        "select_algorithm",
        "Select algorithm",
        [
            "Algorithm 1",
            "Algorithm 2",
            "Provided by me",
        ],
    ),
    ui.panel_conditional(
        "input.select_algorithm == 'Provided by me'",
        ui.input_action_button("edit_algorithm", "Edit algorithm"),
    ),
    ui.input_action_button("run_experiment", "Run experiment"),
    width=320,
    title=ui.input_text("experiment_title", label=None, placeholder="Experiment title"),
)
