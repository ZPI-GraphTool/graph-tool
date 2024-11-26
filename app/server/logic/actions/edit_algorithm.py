import shelve
import shutil
from pathlib import Path

from app.server._config import (
    ALGORITHM_TEMPLATES_DIRECTORY,
    ALGORITHMS_DIRECTORY,
    AlgorithmType,
)

from .open_file import open_file


class AlgorithmTypeSpecification:
    @classmethod
    def new_file(cls, type: AlgorithmType) -> str:
        match type:
            case AlgorithmType.PREPROCESSING:
                prefix = "function"
            case AlgorithmType.BATCH | AlgorithmType.STREAMING:
                prefix = "algorithm"
        # this caches how many files of each type have been created so far
        # so that we know what number to name the new file of a given type
        with shelve.open(ALGORITHMS_DIRECTORY / "counter") as counter:
            key = f"{type}_counter"
            if key not in counter:
                counter[key] = 0
            file_name = f"{prefix}_{counter[key]}.py"
            counter[key] += 1
        return file_name

    @classmethod
    def paths(cls, type: AlgorithmType) -> tuple[Path, Path]:
        template_path = ALGORITHM_TEMPLATES_DIRECTORY / f"template_{type}.py"
        destination_directory = ALGORITHMS_DIRECTORY / type
        destination_directory.mkdir(parents=True, exist_ok=True)
        destination = destination_directory / cls.new_file(type)
        return template_path, destination


def edit_algorithm(option: str, type: AlgorithmType) -> None:
    if option == "New":
        template, destination = AlgorithmTypeSpecification.paths(type)
        new_file_path = shutil.copy(template, destination)
        open_file(new_file_path)
    else:
        open_file(Path(option))
