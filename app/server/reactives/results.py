from datetime import datetime
from pathlib import Path
from typing import Any

import faicons as fa
import pandas as pd
import plotly.express as px
from htmltools import Tag
from plotly.graph_objs import Figure
from shiny import Inputs, reactive, render, ui
from shinywidgets import render_widget

from app.server.logic.actions.save_results import (
    save_results_to_latex,
    save_results_to_markdown,
)
from app.server.logic.runner import Runner

from .selectize import get_class_name_from


def get_experiment_name(experiment_name: str) -> str | Path:
    current_date = Path(datetime.now().strftime("%Y-%m-%d"))
    current_time = Path(datetime.now().strftime("%H_%M_%S"))
    ui.update_text(
        "experiment_name", placeholder=f"{str(current_date)} {str(current_time)}"
    )
    return experiment_name or current_date / current_time


def server_results(input: Inputs, results: dict[str, reactive.Value]):
    @reactive.calc
    def plotly_template() -> str:
        return "plotly_dark" if input.mode() == "dark" else "plotly"

    @reactive.calc
    def get_streaming_node_rank() -> pd.DataFrame:
        return pd.DataFrame(
            results["streaming_results"].get(), columns=["node", "value"]
        )

    @render.ui
    def streaming_node_rank() -> Tag:
        return ui.card(
            ui.card_header("Streaming node rank"),
            render.data_frame(get_streaming_node_rank),
            full_screen=True,
        )

    @reactive.calc
    def get_batch_node_rank() -> pd.DataFrame:
        return pd.DataFrame(results["batch_results"].get(), columns=["node", "value"])

    @render.ui
    def batch_node_rank() -> Tag | None:
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
    def calculation_time_plot() -> Tag:
        return ui.card(
            ui.card_header("Calculation time"),
            render_widget(get_calculation_time_plot),  # type: ignore
            full_screen=True,
        )

    @reactive.calc
    def get_memory_usage_plot() -> Figure:
        edge, memory = zip(*results["memory_usage"].get())
        df = pd.DataFrame({"edge": edge, "memory": memory})
        line_plot = px.line(
            df,
            x="edge",
            y="memory",
            labels={"edge": "edge", "memory": "memory [B]"},
            template=plotly_template(),
        )
        return line_plot

    @render.ui
    def memory_usage_plot() -> Tag:
        return ui.card(
            ui.card_header("Memory usage history"),
            render_widget(get_memory_usage_plot),  # type: ignore
            full_screen=True,
        )

    def get_total_edge_count() -> int:
        runner = results["runner"].get()
        return runner.edge_count

    def get_dataset_size() -> str:
        runner = results["runner"].get()
        size = runner.dataset_size
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size} {unit}"
            size //= 1024
        return "Very large"

    @reactive.calc
    def get_comparison_metrics() -> tuple[float | Any, float | Any, str, int]:
        runner: Runner = results["runner"].get()
        order, cardinality = (
            input.node_rank_order() == "Descending",
            input.node_rank_cardinality(),
        )
        jaccard_similarity = runner.get_jaccard_similarity(order, cardinality)
        streaming_accuracy = runner.get_streaming_accuracy(order, cardinality)
        return (
            jaccard_similarity,
            streaming_accuracy,
            input.node_rank_order(),
            cardinality,
        )

    @render.text
    def total_edge_count() -> str:
        return str(get_total_edge_count())

    @render.text
    def dataset_size() -> str:
        return get_dataset_size()

    @render.text
    def jaccard_similarity() -> str:
        return f"{get_comparison_metrics()[0]:.4g}"

    @render.text
    def streaming_accuracy() -> str:
        return f"{get_comparison_metrics()[1]:.4g}"

    @render.ui
    def metrics_with_batch() -> Tag:
        return ui.card(
            ui.card_header("Properties and metrics"),
            ui.row(
                ui.column(
                    6,
                    ui.value_box(
                        "Total edge count",
                        ui.output_text("total_edge_count"),
                        showcase=fa.icon_svg("circle-nodes", margin_left="2rem"),
                    ),
                ),
                ui.column(
                    6,
                    ui.value_box(
                        "Size of dataset",
                        ui.output_text("dataset_size"),
                        showcase=fa.icon_svg("database", margin_left="2rem"),
                    ),
                ),
                class_="value-box-row",
            ),
            ui.row(
                ui.input_selectize(
                    "node_rank_order",
                    label="Sorting order",
                    choices=["Ascending", "Descending"],
                    width="50%",
                ),
                ui.input_numeric(
                    "node_rank_cardinality",
                    label="Cardinality of node rank",
                    value=10,
                    min=1,
                    width="50%",
                ),
            ),
            ui.row(
                ui.column(
                    6,
                    ui.value_box(
                        "Jaccard similarity",
                        ui.output_text("jaccard_similarity"),
                        showcase=fa.icon_svg("overlap", margin_left="2rem"),
                    ),
                ),
                ui.column(
                    6,
                    ui.value_box(
                        "Streaming accuracy",
                        ui.output_text("streaming_accuracy"),
                        showcase=fa.icon_svg("bullseye", margin_left="2rem"),
                    ),
                ),
                class_="value-box-row",
            ),
            height="100%",
        )

    @render.ui
    def metrics_no_batch() -> Tag:
        return ui.card(
            ui.card_header("Properties"),
            ui.value_box(
                "Total edge count",
                ui.output_text("total_edge_count"),
                showcase=fa.icon_svg("circle-nodes", margin_left="2rem"),
            ),
            ui.tags.div(class_="flex-divider"),
            ui.value_box(
                "Size of dataset",
                ui.output_text("dataset_size"),
                showcase=fa.icon_svg("database", margin_left="2rem"),
            ),
        )

    @render.ui
    @reactive.event(input.run_experiment)
    def results_first_row() -> Tag:
        columns = (
            (
                ui.output_ui("streaming_node_rank"),
                ui.output_ui("batch_node_rank"),
                ui.output_ui("metrics_with_batch"),
            )
            if input.with_batch()
            else (
                ui.output_ui("streaming_node_rank"),
                ui.output_ui("calculation_time_plot"),
            )
        )
        return ui.layout_columns(
            *columns,
            max_height="48%",
            col_widths=[3, 3, 6] if input.with_batch() else [3, 9],
        )

    @render.ui
    @reactive.event(input.run_experiment)
    def results_second_row() -> Tag:
        columns = (
            (
                ui.output_ui("memory_usage_plot"),
                ui.output_ui("calculation_time_plot"),
            )
            if input.with_batch()
            else (ui.output_ui("metrics_no_batch"), ui.output_ui("memory_usage_plot"))
        )
        return ui.layout_columns(
            *columns,
            max_height="49%",
            col_widths=[6, 6] if input.with_batch() else [3, 9],
        )

    @render.ui
    @reactive.event(input.run_experiment)
    def save_results_button() -> tuple[Tag, Tag]:
        return (
            ui.input_radio_buttons(
                "output_format",
                "Output format",
                ["LaTeX", "Markdown"],
                selected="LaTeX",
                inline=True,
            ),
            ui.input_task_button(
                "save_results",
                "Save results",
                icon=fa.icon_svg("floppy-disk"),
                label_busy="Saving...",
                class_="btn-outline-success",
            ),
        )

    @ui.bind_task_button(button_id="save_results")
    @reactive.extended_task
    async def save_results_task(output_format: str, **kwargs) -> None:
        output_format = output_format.lower()
        if output_format == "markdown":
            save_results_to_markdown(**kwargs)
        elif output_format == "latex":
            save_results_to_latex(**kwargs)
        else:
            raise NotImplementedError(f"Output format {output_format} is not supported")

    @reactive.effect
    @reactive.event(input.save_results)
    def _() -> None:
        (
            preprocessing_function,
            batch_algorithm,
            jaccard_similarity,
            streaming_accuracy,
            order,
            cardinality,
            batch_node_rank,
        ) = None, None, None, None, None, None, None
        if input.with_preprocessing() and input.select_preprocessing() != "New":
            preprocessing_function = input.select_preprocessing()
        if input.with_batch():
            batch_algorithm = get_class_name_from(input.select_batch())
            jaccard_similarity, streaming_accuracy, order, cardinality = (
                get_comparison_metrics()
            )
            batch_node_rank = get_batch_node_rank()

        save_results_task(
            output_format=input.output_format(),
            experiment_name=input.experiment_name(),
            preprocessing_function=preprocessing_function,
            streaming_algorithm=get_class_name_from(input.select_streaming()),
            batch_algorithm=batch_algorithm,
            total_edge_count=get_total_edge_count(),
            dataset_size=get_dataset_size(),
            order=order,
            cardinality=cardinality,
            jaccard_similarity=jaccard_similarity,
            streaming_accuracy=streaming_accuracy,
            streaming_node_rank=get_streaming_node_rank(),
            batch_node_rank=batch_node_rank,
            calculation_time=get_calculation_time_plot(),
            memory_usage=get_memory_usage_plot(),
        )
