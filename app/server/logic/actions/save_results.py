from datetime import datetime
from pathlib import Path

from plotly.graph_objs import Figure

from .open_file_in_editor import open_file_in_editor

EXPERIMENTS_DIRECTORY = Path(__file__).parents[4] / "experiments"


def dedent(message: str) -> str:
    content: str = "# Results\n"
    for line in message.splitlines():
        content += line.lstrip() + "\n"
    return content


def get_save_directory(experiment_name: str):
    current_date = Path(datetime.now().strftime("%Y-%m-%d"))
    current_time = Path(datetime.now().strftime("%H_%M_%S"))
    experiment_path = experiment_name or current_date / current_time
    save_directory = EXPERIMENTS_DIRECTORY / experiment_path
    # make sure the directory exists
    save_directory.mkdir(parents=True, exist_ok=True)
    return save_directory


def save_plot_images(plots: list, save_directory: Path) -> str:
    results = ""
    for name, plot in plots:
        plot: Figure
        images_directory = save_directory / "images"
        images_directory.mkdir(exist_ok=True)
        image_file = f"{name}.svg"
        path = images_directory / image_file
        plot.write_image(path)
        results += f"\n\n![{name}](images/{image_file})\n"
    return results


def save_results(experiment_name: str, results: str, plots: list) -> None:
    save_directory = get_save_directory(experiment_name)
    results += save_plot_images(plots, save_directory)
    save_file = save_directory / "results.md"
    content = dedent(results)
    with Path.open(save_file, "w", encoding="utf-8") as file:
        file.write(content)
    open_file_in_editor(save_file)
