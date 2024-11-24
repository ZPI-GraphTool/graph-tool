from datetime import datetime
from pathlib import Path

from plotly.graph_objs import Figure

from app.server._config import EXPERIMENTS_DIRECTORY

from .open_file import open_file

PlotList = list[tuple[str, Figure]]


def dedent(message: str) -> str:
    content: str = "# Results\n\n"
    for line in message.splitlines():
        content += line.lstrip() + "\n"
    return content


def get_results_directory(experiment_name: str):
    current_date = Path(datetime.now().strftime("%Y-%m-%d"))
    current_time = Path(datetime.now().strftime("%H_%M_%S"))
    experiment_path = experiment_name or current_date / current_time
    results_directory = EXPERIMENTS_DIRECTORY / experiment_path
    # make sure the directory exists
    results_directory.mkdir(parents=True, exist_ok=True)
    return results_directory


def write_plot_images(plots: PlotList, results_directory: Path) -> str:
    results = ""
    for name, plot in plots:
        images_directory = results_directory / "images"
        images_directory.mkdir(exist_ok=True)
        image_file = f"{name}.svg"
        plot.write_image(images_directory / image_file)
        results += f"\n![{name}](images/{image_file})\n"
    return results


def save_results(experiment_name: str, results: str, plots: list) -> None:
    results_directory = get_results_directory(experiment_name)
    results += write_plot_images(plots, results_directory)
    results_file = results_directory / "results.md"
    with Path.open(results_file, "w", encoding="utf-8") as file:
        file.write(dedent(results))
    open_file(results_file)
