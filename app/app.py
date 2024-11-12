# Load data and compute static values
from server import server
from shiny import App
from ui import app_ui

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
