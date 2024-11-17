from pathlib import Path
import traceback 
import sys

import pandas as pd
import plotly.express as px
from demos import CONNECTIONS_CSV_FILE
from shiny import reactive, render, ui
from shinywidgets import render_widget

from .logic import Runner
from .logic.actions import AlgorithmType, edit_algorithm, save_results
from .reactives import (
    server_batch_selectize,
    server_preprocessing_selectize,
    server_streaming_selectize,
)

results = reactive.value()



def server(input, output, session):
    server_batch_selectize(input)
    server_preprocessing_selectize(input)
    server_streaming_selectize(input)
    
    errors = reactive.value()

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

    @reactive.calc
    def select_dataset() -> Path:
        match input.select_dataset():
            case "0":
                dataset_path = Path(input.dataset_path())
            case "1":
                dataset_path = CONNECTIONS_CSV_FILE
        return dataset_path

    @reactive.effect
    @reactive.event(input.run_experiment)
    def run_experiment():
        dataset_path = select_dataset()
        preprocess_path = (
            input.select_preprocessing() if input.with_preprocessing() else None
        )
        streaming_path = input.select_streaming()
        batch_path = input.select_batch() if input.with_batch() else None

        try: 
            runner = Runner(
                dataset_path=dataset_path,
                preprocess_path=preprocess_path,
                streaming_path=streaming_path,
                batch_path=batch_path,
            )
            runner.validate_implementation()
            results.set(runner.run())
        except Exception as ex: 
            errors.set(ex)

    @reactive.calc
    def streaming_node_rank():
        streaming_results, *_ = results.get()
        df = pd.DataFrame(streaming_results, columns=["node", "value"])
        return df.head(20)

    @render.data_frame
    def render_streaming_node_rank():
        return render.DataGrid(streaming_node_rank())

    @reactive.calc
    def avg_property_time_per_edge_plot():
        *_, avg_property_time_per_edge, _ = results.get()
        df = pd.DataFrame(avg_property_time_per_edge, columns=["time"])
        line_plot = px.line(
            df, x=df.index, y="time", title="Average property time per edge"
        )
        return line_plot

    @render_widget  # type: ignore
    def render_avg_property_time_per_edge_plot():
        return avg_property_time_per_edge_plot()

    @reactive.effect
    @reactive.event(input.save_results)
    def _():
        streaming_nr = streaming_node_rank().to_markdown()
        results = streaming_nr
        avg_property_time_plot = (
            "avg_property_time_per_edge",
            avg_property_time_per_edge_plot(),
        )
        plots = [avg_property_time_plot]
        experiment_name = input.experiment_name()
        save_results(experiment_name, results, plots)


    @reactive.effect
    @reactive.event(errors)
    def modal_error_display():
        
        m = ui.modal(
            str(errors.get()),
            title = "Error",
            easy_close=True
        )
        ui.modal_show(m)
