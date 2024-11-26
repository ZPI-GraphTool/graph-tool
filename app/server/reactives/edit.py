from shiny import Inputs, reactive

from app.server._config import AlgorithmType
from app.server.logic.actions import edit_algorithm


def server_edit(input: Inputs) -> None:
    @reactive.effect
    @reactive.event(input.edit_preprocessing)
    def _() -> None:
        edit_algorithm(input.select_preprocessing(), AlgorithmType.PREPROCESSING)

    @reactive.effect
    @reactive.event(input.edit_streaming)
    def _() -> None:
        edit_algorithm(input.select_streaming(), AlgorithmType.STREAMING)

    @reactive.effect
    @reactive.event(input.edit_batch)
    def _() -> None:
        edit_algorithm(input.select_batch(), AlgorithmType.BATCH)
