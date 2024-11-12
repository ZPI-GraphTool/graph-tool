from demos import DEGREE_CENTRALITY_STREAM_ALGORITHM_FILE
from shiny import reactive, render, ui

from .utils import get_algorithm_names


def server_streaming_selectize(input):
    @render.ui
    @reactive.event(input.refresh_streaming_list, ignore_none=False)
    def streaming_selectize():
        return (
            ui.input_selectize(
                "select_streaming",
                "",
                {
                    "": {"New": "New algorithm"},
                    "Existing": get_algorithm_names("streaming"),
                    "Presupplied": {
                        str(
                            DEGREE_CENTRALITY_STREAM_ALGORITHM_FILE
                        ): "Degree centrality stream",
                    },
                },
                selected=str(DEGREE_CENTRALITY_STREAM_ALGORITHM_FILE),
            ),
        )
