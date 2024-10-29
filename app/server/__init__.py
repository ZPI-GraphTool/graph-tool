import asyncio
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from shiny import reactive, render, ui
from static import TIPS_CSV_FILE

from .logic.actions import edit_algorithm, save_results


def server(input, output, session):
    @reactive.effect
    @reactive.event(input.edit_algorithm)
    def _():
        edit_algorithm()

    @reactive.calc
    def parse_file():
        dataset_path: Path
        match input.select_dataset():
            case "0":
                dataset_path = input.dataset_path()
            case "1":
                dataset_path = TIPS_CSV_FILE
            case "2":
                pass
        return pd.read_csv(dataset_path)

    @output
    @render.ui
    @reactive.event(input.run_experiment)
    async def compute():
        data = parse_file()
        if input.preprocess_data():
            # TODO: Preprocess data
            ...
        with ui.Progress(min=0, max=15) as progress:
            progress.set(
                message="Calculation in progress", detail="This may take a while..."
            )
            for i in range(15):
                progress.set(i, message="Computing")
                await asyncio.sleep(0.1)
        print(data)

    @reactive.effect
    @reactive.event(input.save_results)
    def _():
        save_results()

    @render.plot
    def plot():
        some_dist = pd.Series([1, 2, 3, 4, 5])

        fig, ax = plt.subplots()
        ax.hist(some_dist)
        plt.savefig("plot.png")
        return fig
