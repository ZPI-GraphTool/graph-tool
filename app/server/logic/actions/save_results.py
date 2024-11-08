import textwrap
from pathlib import Path

from .open_file_in_editor import open_file_in_editor

ROOT_DIRECTORY = Path(__file__).parent


def get_content(results: str) -> str:
    return textwrap.dedent(f"""\
        ## Results
        {results}
    """)


def save_results(results: str = "Some metric: 0.123\n") -> None:
    save_file_path = ROOT_DIRECTORY / "results.md"
    content = get_content(results)
    with Path.open(save_file_path, "w") as file:
        file.write(content)
    open_file_in_editor(save_file_path)
