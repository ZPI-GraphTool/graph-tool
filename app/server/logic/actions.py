# ruff: noqa: D100, D103

import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT_DIRECTORY = Path(__file__).parent


def open_file_in_editor(file_path: Path) -> None:
    try:
        subprocess.call(["code", file_path])
    except FileNotFoundError:
        if sys.platform == "win32":
            os.startfile(file_path)  # noqa: S606
        else:
            open_command = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([open_command, file_path])  # noqa: S603


def duplicate_file(file_path: Path, destination: Path) -> Path:
    return shutil.copy(file_path, destination)


def edit_algorithm() -> None:
    new_file_count = 0

    template_path = ROOT_DIRECTORY / "template.py"
    destination = ROOT_DIRECTORY / "functions" / f"function{new_file_count + 1}.py"

    new_file_path = duplicate_file(template_path, destination)
    open_file_in_editor(new_file_path)


def get_content(results: str) -> str:
    return textwrap.dedent(f"""\
        ## Results
        {results}\
    """)


def save_results(results: str = "Some metric: 0.123\n") -> None:
    save_file_path = ROOT_DIRECTORY / "results.md"
    content = get_content(results)
    with Path.open(save_file_path, "w") as file:
        file.write(content)
    open_file_in_editor(save_file_path)
