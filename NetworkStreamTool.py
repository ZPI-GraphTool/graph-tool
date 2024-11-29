import webbrowser
from pathlib import Path
from threading import Thread

from PIL import Image
from pystray import Icon
from pystray import MenuItem as item

from app import kill_python, shiny_app

STATIC_DIRECTORY = Path(__file__).parent / "_static"


def open_app_in_browser():
    webbrowser.open("http://localhost:8000")


if __name__ == "__main__":
    run_shiny_app = Thread(target=shiny_app.run)
    run_shiny_app.start()

    image = Image.open(STATIC_DIRECTORY / "icon.png")
    menu = (
        item("Open app", open_app_in_browser),
        item("Quit", kill_python),
    )
    systray_icon = Icon("nst-app", image, "Network Stream Tool", menu)

    open_app_in_browser()

    systray_icon.run()
