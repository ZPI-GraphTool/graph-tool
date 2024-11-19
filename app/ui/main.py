from shiny import ui

from .sidebar import sidebar
from .static import STYLES_CSS_FILE

app_ui = ui.page_sidebar(
    sidebar,
    ui.panel_conditional(
        "input.with_batch == true",
        ui.layout_columns(
            ui.output_ui("streaming_node_rank"),
            ui.output_ui("batch_node_rank"),
            ui.output_ui("memory_history_plot"),
            max_height="50%",
            col_widths=[3, 3, 6],
        ),
    ),
    ui.panel_conditional(
        "input.with_batch == false",
        ui.layout_columns(
            ui.output_ui("streaming_node_rank"),
            ui.output_ui("memory_history_plot"),
            max_height="50%",
            col_widths=[3, 9],
        ),
    ),
    ui.panel_conditional(
        "input.with_preprocessing == true",
        ui.layout_columns(
            ui.output_ui("preprocessing_time_plot"),
            ui.output_ui("calculation_time_plot"),
            col_widths=[6, 6],
        ),
    ),
    ui.panel_conditional(
        "input.with_preprocessing == false",
        ui.output_ui("calculation_time_plot"),
    ),
    ui.include_css(STYLES_CSS_FILE),
    title="Network Stream Tool",
    fillable=True,
    class_="bslib-page-dashboard",
)
