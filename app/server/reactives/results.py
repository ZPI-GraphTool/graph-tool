import faicons as fa
import pandas as pd
import plotly.express as px
from htmltools import Tag
from plotly.graph_objs import Figure
from shiny import Inputs, reactive, render, ui
from shinywidgets import render_widget

from ..logic.actions import save_results


def server_results(input: Inputs, results: dict[str, reactive.Value]):
    @reactive.calc
    def plotly_template() -> str:
        return "plotly_dark" if input.mode() == "dark" else "plotly"

    @reactive.calc
    def get_streaming_node_rank() -> pd.DataFrame:
        return pd.DataFrame(results["streaming"].get(), columns=["node", "value"])

    @render.ui
    @reactive.event(input.run_experiment)
    def streaming_node_rank() -> Tag:
        return ui.card(
            ui.card_header("Streaming node rank"),
            render.data_frame(get_streaming_node_rank),
            full_screen=True,
        )

    @reactive.calc
    def get_batch_node_rank() -> pd.DataFrame:
        return pd.DataFrame(results["batch"].get(), columns=["node", "value"])

    @render.ui
    @reactive.event(input.run_experiment)
    def batch_node_rank() -> Tag | None:
        if not input.with_batch():
            return None
        return ui.card(
            ui.card_header("Batch node rank"),
            render.data_frame(get_batch_node_rank),
            full_screen=True,
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
    def calculation_time_plot() -> Tag:
        return ui.card(
            ui.card_header("Calculation time"),
            render_widget(get_calculation_time_plot),  # type: ignore
            full_screen=True,
        )

    @reactive.calc
    def get_memory_history_plot() -> Figure:
        df = pd.DataFrame(results["memory"].get(), columns=["memory [B]"])
        line_plot = px.line(
            df,
            y=df.columns.values[0],
            labels={"index": "edge"},
            template=plotly_template(),
        )
        return line_plot

    @render.ui
    @reactive.event(input.run_experiment)
    def memory_history_plot() -> Tag:
        return ui.card(
            ui.card_header("Memory history"),
            render_widget(get_memory_history_plot),  # type: ignore
            full_screen=True,
        )

    @render.ui
    @reactive.event(input.run_experiment)
    def results_first_row() -> Tag:
        columns = (
            (
                ui.output_ui("streaming_node_rank"),
                ui.output_ui("batch_node_rank"),
                ui.output_ui("memory_history_plot"),
            )
            if input.with_batch()
            else (
                ui.output_ui("streaming_node_rank"),
                ui.output_ui("memory_history_plot"),
            )
        )
        return ui.layout_columns(
            *columns,
            max_height="50%",
            col_widths=[3, 3, 6] if input.with_batch() else [3, 9],
        )

    @render.ui
    @reactive.event(input.run_experiment)
    def save_results_button() -> Tag:
        return ui.input_action_button(
            "save_results",
            "Save results",
            icon=fa.icon_svg("floppy-disk"),
            class_="btn-outline-success",
        )

    @reactive.effect
    @reactive.event(input.save_results)
    def _() -> None:
        results = get_streaming_node_rank().to_markdown() + "\n"
        if input.with_batch():
            results += get_batch_node_rank().to_markdown() + "\n"
        calculation_time_plot = (
            "calculation_time_per_edge",
            get_calculation_time_plot(),
        )
        memory_history_plot = ("memory_history", get_memory_history_plot())
        plots = [calculation_time_plot, memory_history_plot]
        save_results(input.experiment_name(), results, plots)
