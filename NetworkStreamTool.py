import webbrowser
from threading import Thread

from app import shiny_app

if __name__ == "__main__":
    run_shiny_app = Thread(target=shiny_app.run)
    run_shiny_app.start()
    webbrowser.open("http://localhost:8000")
    run_shiny_app.join()
