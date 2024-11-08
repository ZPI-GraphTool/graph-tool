from shiny import ui

from .partials import sidebar
from .static import STYLES_CSS_FILE

app_ui = ui.page_sidebar(
    sidebar,
    ui.output_ui("compute"),
    # ui.output_plot("plot"),
    ui.include_css(STYLES_CSS_FILE),
    title="Network Stream Tool",
    fillable=True,
)
