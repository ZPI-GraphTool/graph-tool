from shiny import ui
from shinywidgets import output_widget

from .sidebar import sidebar
from .static import STYLES_CSS_FILE

app_ui = ui.page_sidebar(
    sidebar,
    ui.output_data_frame("render_streaming_node_rank"),
    output_widget("render_avg_property_time_per_edge_plot"),
    ui.include_css(STYLES_CSS_FILE),
    title="Network Stream Tool",
    fillable=True,
)
