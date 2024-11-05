from pathlib import Path

from shiny import ui

offset = 2  # How many algorithms are supplied by default


def get_algorithm_names() -> dict[str, str]:
    algorithm_names: dict[str, str] = {}
    algorithms_directory = Path(__file__).parents[1] / "server" / "algorithms"
    for i, algorithm_file in enumerate(algorithms_directory.glob("*.py")):
        print(algorithm_file)
        with open(algorithm_file, encoding="utf-8") as file:
            algorithm_name = file.readline().lstrip("#").strip()
            algorithm_names.update({str(i + offset): algorithm_name})
    return algorithm_names


sidebar = ui.sidebar(
    ui.input_selectize(
        "select_dataset",
        "Select dataset",
        {
            "Supplied": {"1": "Dataset 1", "2": "Dataset 2"},
            "Provided by me": {"0": "Custom dataset"},
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
    ui.input_selectize(
        "select_algorithm",
        "Select algorithm",
        {
            "Supplied": {"0": "Algorithm 1", "1": "Algorithm 2"},
            "Provided by me": get_algorithm_names(),
        },
    ),
    ui.panel_conditional(
        "input.select_algorithm == 'Provided by me'",
        ui.input_action_button("edit_algorithm", "Edit algorithm"),
    ),
    ui.input_action_button("run_experiment", "Run experiment"),
    width=320,
    title=ui.input_text("experiment_title", label=None, placeholder="Experiment title"),
)
