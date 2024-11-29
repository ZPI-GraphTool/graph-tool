from shiny import App

from .server import kill_python, server
from .ui import STATIC_DIRECTORY, app_ui

__all__ = ["kill_python", "shiny_app"]


shiny_app = App(app_ui, server, static_assets=STATIC_DIRECTORY)
