from shiny import App

from .server import server
from .ui import app_ui, static_assets

shiny_app = App(app_ui, server, static_assets=static_assets)
