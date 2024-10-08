# ruff: noqa: D100, D103

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIRECTORY = Path(__file__).parent


def open_new_file_in_editor(file_path: Path) -> None:
    try:
        subprocess.call(["code", file_path])
    except FileNotFoundError:
        if sys.platform == "win32":
            os.startfile(file_path)  # noqa: S606
        else:
            open_command = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([open_command, file_path])  # noqa: S603


def duplicate_file(file_path: Path, new_file_name: str) -> Path:
    new_file_path = ROOT_DIRECTORY / "functions" / new_file_name
    shutil.copy(file_path, new_file_path)
    return new_file_path


def edit_function_logic():
    new_file_count = 0
    template_path = ROOT_DIRECTORY / "template.py"
    new_file_name = f"function{new_file_count + 1}.py"
    new_file_path = duplicate_file(template_path, new_file_name)
    open_new_file_in_editor(new_file_path)
