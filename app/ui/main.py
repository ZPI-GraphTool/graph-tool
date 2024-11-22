from shiny import ui

from .sidebar import sidebar
from .static import STYLES_CSS_FILE

app_ui = ui.page_sidebar(
    sidebar,
    ui.output_ui("results_first_row"),
    ui.output_ui("calculation_time_plot"),
    ui.include_css(STYLES_CSS_FILE),
    title="Network Stream Tool",
    fillable=True,
    class_="bslib-page-dashboard",
)
