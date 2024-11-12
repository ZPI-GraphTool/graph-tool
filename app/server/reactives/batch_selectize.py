from demos import DEGREE_CENTRALITY_BATCH_ALGORITHM_FILE
from shiny import reactive, render, ui

from .utils import get_algorithm_names


def server_batch_selectize(input):
    @render.ui
    @reactive.event(input.refresh_batch_list, ignore_none=False)
    def batch_selectize():
        return (
            ui.input_selectize(
                "select_batch",
                "",
                {
                    "": {"New": "New algorithm"},
                    "Existing": get_algorithm_names("batch"),
                    "Presupplied": {
                        str(
                            DEGREE_CENTRALITY_BATCH_ALGORITHM_FILE
                        ): "Degree centrality batch",
                    },
                },
                selected=str(DEGREE_CENTRALITY_BATCH_ALGORITHM_FILE),
            ),
        )
