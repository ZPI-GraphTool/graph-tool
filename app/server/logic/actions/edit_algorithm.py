import shutil
from pathlib import Path

from app.server._config import (
    PREDEFINED_ALGORITHMS,
    AlgorithmType,
    AlgorithmTypeSpecification,
)

from .open_file import open_file


def edit_algorithm(
    option: str, algorithm_type: AlgorithmType, dataset_type: str
) -> None:
    if option == "New":
        template, destination = AlgorithmTypeSpecification.paths(algorithm_type)
        new_file_path = shutil.copy(template, destination)

        with open(new_file_path) as f:
            contents = f.readlines()
        message = AlgorithmTypeSpecification.get_type_hint_message(
            algorithm_type, dataset_type
        )
        contents.insert(11, message)

        with open(new_file_path, "w") as f:
            f.writelines(contents)

        open_file(new_file_path)
    else:
        algorithm_path = Path(option).resolve()
        if algorithm_path in PREDEFINED_ALGORITHMS:
            _, destination = AlgorithmTypeSpecification.paths(algorithm_type)
            new_file_path = shutil.copy(option, destination)
            open_file(new_file_path)
        else:
            open_file(Path(option))
