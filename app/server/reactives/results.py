import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure
from shiny import reactive, render
from shinywidgets import render_widget

from ..logic.actions import save_results


def server_results(input, results: dict[str, reactive.value]):
    @reactive.calc
    def get_streaming_node_rank() -> pd.DataFrame:
        df = pd.DataFrame(results["streaming"].get(), columns=["node", "value"])
        return df.head(20)

    @render.data_frame
    def render_streaming_node_rank() -> render.DataGrid:
        return render.DataGrid(get_streaming_node_rank())

    @reactive.calc
    def get_calculation_time_plot() -> Figure:
        df = pd.DataFrame(results["calculation_time"].get(), columns=["time [ns]"])
        line_plot = px.line(
            df,
            y=df.columns.values[0],
            title="Average calculation time per edge",
            labels={"index": "edge"},
        )
        return line_plot

    @render_widget  # type: ignore
    def render_calculation_time_plot() -> Figure:
        return get_calculation_time_plot()

    @reactive.calc
    def get_memory_history_plot():
        df = pd.DataFrame(results["memory"].get(), columns=["memory"])
        line_plot = px.line(
            df,
            y=df.columns.values[0],
            title="Memory history",
            labels={"index": "edge"},
        )
        return line_plot

    @render_widget  # type: ignore
    def render_memory_history_plot() -> Figure:
        return get_memory_history_plot()

    @reactive.effect
    @reactive.event(input.save_results)
    def _():
        streaming_nr = get_streaming_node_rank().to_markdown()
        results = streaming_nr
        calculation_time_plot = (
            "calculation_time_per_edge",
            get_calculation_time_plot(),
        )
        plots = [calculation_time_plot]
        save_results(input.experiment_name(), results, plots)
