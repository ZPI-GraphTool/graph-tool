from shiny import reactive, render, ui

from .utils import get_algorithm_names


def server_preprocessing_selectize(input):
    @render.ui
    @reactive.event(input.refresh_preprocessing_list, ignore_none=False)
    def preprocessing_selectize():
        return (
            ui.input_selectize(
                "select_preprocessing",
                "",
                {
                    "": {"New": "New function"},
                    "Existing": get_algorithm_names("preprocessing"),
                },
                selected="New",
            ),
        )
