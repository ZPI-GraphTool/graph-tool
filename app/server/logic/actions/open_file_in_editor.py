import os
import subprocess
import sys
from pathlib import Path


def open_file_in_editor(file_path: Path) -> None:
    try:
        subprocess.call(["code", file_path])
    except FileNotFoundError:
        if sys.platform == "win32":
            os.startfile(file_path)  # noqa: S606
        else:
            open_command = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([open_command, file_path])  # noqa: S603
