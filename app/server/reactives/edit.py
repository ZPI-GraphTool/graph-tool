from shiny import reactive

from ..logic.actions import AlgorithmType, edit_algorithm


def server_edit(input):
    @reactive.effect
    @reactive.event(input.edit_preprocessing)
    def _():
        edit_algorithm(input.select_preprocessing(), AlgorithmType.PREPROCESSING)

    @reactive.effect
    @reactive.event(input.edit_streaming)
    def _():
        edit_algorithm(input.select_streaming(), AlgorithmType.STREAMING)

    @reactive.effect
    @reactive.event(input.edit_batch)
    def _():
        edit_algorithm(input.select_batch(), AlgorithmType.BATCH)
