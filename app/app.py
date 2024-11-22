# Load data and compute static values
from server import server
from shiny import App
from ui import app_ui, static_assets

app = App(app_ui, server, static_assets=static_assets)

if __name__ == "__main__":
    app.run()
