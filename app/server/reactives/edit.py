from random import random

from shiny import Inputs, reactive

from app.server._config import AlgorithmType
from app.server.logic.actions import edit_algorithm

from .run_experiment import MissingPathError, get_paths


def server_edit(input: Inputs, errors: reactive.Value) -> None:
    @reactive.effect
    @reactive.event(input.edit_preprocessing)
    def _() -> None:
        try:
            dataset_path, _, _, _ = get_paths(input)
        except MissingPathError as mpe:
            errors.set((random(), str(mpe)))
        else:
            edit_algorithm(
                input.select_preprocessing(),
                AlgorithmType.PREPROCESSING,
                dataset_path.suffix,
            )

    @reactive.effect
    @reactive.event(input.edit_streaming)
    def _() -> None:
        try:
            dataset_path, _, _, _ = get_paths(input)
        except MissingPathError as mpe:
            errors.set((random(), str(mpe)))
        else:
            edit_algorithm(
                input.select_streaming(),
                AlgorithmType.STREAMING,
                dataset_path.suffix,
            )

    @reactive.effect
    @reactive.event(input.edit_batch)
    def _() -> None:
        try:
            dataset_path, _, _, _ = get_paths(input)
        except MissingPathError as mpe:
            errors.set((random(), str(mpe)))
        else:
            edit_algorithm(
                input.select_batch(),
                AlgorithmType.BATCH,
                dataset_path.suffix,
            )
