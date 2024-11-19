import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure, Layout
from shiny import reactive, render, ui
from shinywidgets import render_widget

from ..logic.actions import save_results

test_template = dict(layout=Layout())


def server_results(input, results: dict[str, reactive.value]):
    @reactive.calc
    def plotly_template() -> str:
        return "plotly_dark" if input.mode() == "dark" else "plotly"

    @reactive.calc
    def get_streaming_node_rank() -> pd.DataFrame:
        return pd.DataFrame(results["streaming"].get(), columns=["node", "value"])

    @render.ui
    @reactive.event(input.run_experiment)
    def streaming_node_rank():
        return (
            ui.card(
                ui.card_header("Streaming node rank"),
                render.data_frame(get_streaming_node_rank),
                full_screen=True,
            ),
        )

    @reactive.calc
    def get_batch_node_rank() -> pd.DataFrame:
        return pd.DataFrame(results["batch"].get(), columns=["node", "value"])

    @render.ui
    @reactive.event(input.run_experiment)
    def batch_node_rank():
        return (
            (
                ui.card(
                    ui.card_header("Batch node rank"),
                    render.data_frame(get_batch_node_rank),
                    full_screen=True,
                ),
            )
            if input.with_batch()
            else None
        )

    @reactive.calc
    def get_preprocessing_time_plot() -> Figure:
        df = pd.DataFrame(results["preprocessing_time"].get(), columns=["time [ns]"])
        line_plot = px.line(
            df,
            y=df.columns.values[0],
            labels={"index": "edge"},
            template=plotly_template(),
        )
        return line_plot

    @render.ui
    @reactive.event(input.run_experiment)
    def preprocessing_time_plot():
        return (
            (
                ui.card(
                    ui.card_header("Preprocessing time"),
                    render_widget(get_preprocessing_time_plot),  # type: ignore
                    full_screen=True,
                ),
            )
            if input.with_preprocessing()
            else None
        )

    @reactive.calc
    def get_calculation_time_plot() -> Figure:
        df = pd.DataFrame(results["calculation_time"].get(), columns=["time [ns]"])
        line_plot = px.line(
            df,
            y=df.columns.values[0],
            labels={"index": "edge"},
            template=plotly_template(),
        )
        return line_plot

    @render.ui
    @reactive.event(input.run_experiment)
    def calculation_time_plot():
        return (
            ui.card(
                ui.card_header("Calculation time"),
                render_widget(get_calculation_time_plot),  # type: ignore
                full_screen=True,
            ),
        )

    @reactive.calc
    def get_memory_history_plot() -> Figure:
        df = pd.DataFrame(results["memory"].get(), columns=["memory [MB]"])
        line_plot = px.line(
            df,
            y=df.columns.values[0],
            labels={"index": "edge"},
            template=plotly_template(),
        )
        return line_plot

    @render.ui
    @reactive.event(input.run_experiment)
    def memory_history_plot():
        return (
            ui.card(
                ui.card_header("Memory history"),
                render_widget(get_memory_history_plot),  # type: ignore
                full_screen=True,
            ),
        )

    @reactive.effect
    @reactive.event(input.save_results)
    def _():
        results = get_streaming_node_rank().to_markdown() + "\n"
        results += get_batch_node_rank().to_markdown() + "\n"
        preprocessing_time_plot = (
            "preprocessing_time_per_edge",
            get_preprocessing_time_plot(),
        )
        calculation_time_plot = (
            "calculation_time_per_edge",
            get_calculation_time_plot(),
        )
        memory_history_plot = ("memory_history", get_memory_history_plot())
        plots = [preprocessing_time_plot, calculation_time_plot, memory_history_plot]
        save_results(input.experiment_name(), results, plots)
