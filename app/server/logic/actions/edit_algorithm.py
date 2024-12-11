import shelve
import shutil
from pathlib import Path

from app.server._config import (
    ALGORITHM_TEMPLATES_DIRECTORY,
    ALGORITHMS_DIRECTORY,
    PREDEFINED_ALGORITHMS,
    AlgorithmType,
)

from .open_file import open_file


class AlgorithmTypeSpecification:
    @classmethod
    def new_file(cls, algorithm_type: AlgorithmType) -> str:
        prefix: str = ""
        match algorithm_type:
            case AlgorithmType.STREAMING:
                prefix = "streaming_algorithm"
            case AlgorithmType.BATCH:
                prefix = "batch_algorithm"
            case AlgorithmType.PREPROCESSING:
                prefix = "preprocessing_function"
        # this caches how many files of each type have been created so far
        # so that we know what number to name the new file of a given type
        with shelve.open(ALGORITHMS_DIRECTORY / "counter") as counter:
            key = f"{algorithm_type}_counter"
            if key not in counter:
                counter[key] = 0
            file_name = f"{prefix}_{counter[key]}.py"
            counter[key] += 1
        return file_name

    @classmethod
    def paths(cls, algorithm_type: AlgorithmType) -> tuple[Path, Path]:
        template_path = ALGORITHM_TEMPLATES_DIRECTORY / f"template_{algorithm_type}.py"
        destination_directory = ALGORITHMS_DIRECTORY / algorithm_type
        destination_directory.mkdir(parents=True, exist_ok=True)
        destination = destination_directory / cls.new_file(algorithm_type)
        return template_path, destination

    @classmethod
    def get_type_hint_message(
        cls, algorithm_type: AlgorithmType, dataset_type: str
    ) -> str:
        message = ""

        match algorithm_type, dataset_type[1:]:
            case AlgorithmType.BATCH, "csv":
                message = "\t# The dataframe's columns are the headers of the supplied .csv file.\n"
            case AlgorithmType.BATCH, "mtx":
                message = "\t# The dataframe's columns are: 0 - source node, 1 - destination node, (optionally) 2 - weight of the edge.\n"
            case AlgorithmType.BATCH, _:
                message = "\t# The dataframe only has one column 0 unless a specified preprocessing method has been supplied which converts the string line into an object (like a tuple). In that case it follows how pandas creates DataFrames based on a list of those objects\n"

            case _, "csv":
                message = "\t# The edge is a dictionary. Its keys are the headers of the supplied .csv file.\n"
            case _, "mtx":
                message = "\t# The given edge is a tuple. Access its data by indexing: 0 - source node, 1 - destination node, (optionally) 2 - weight of the edge.\n"
            case _, _:
                message = "\t# The edge is a string unless a specified preprocessing method has been supplied. In the latter case the format of the edge matches the return of the preprocessing method.\n"

        return message


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
