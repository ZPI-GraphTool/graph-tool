from shiny import ui

from ._static import STATIC_DIR, STYLES_CSS_FILE
from .sidebar import sidebar

static_assets = STATIC_DIR

app_ui = ui.page_sidebar(
    sidebar,
    ui.head_content(
        ui.tags.link(rel="icon", href="/favicon.png"),
        ui.include_css(STYLES_CSS_FILE),
    ),
    ui.output_ui("results_first_row"),
    ui.output_ui("results_second_row"),
    title="Network Stream Tool",
    fillable=True,
    class_="bslib-page-dashboard",
)
