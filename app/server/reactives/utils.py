import importlib.util
import inspect
import os
import sys
from pathlib import Path


def get_class_name_from(file_path: Path) -> str | None:
    module_name = os.path.basename(file_path)

    spec = importlib.util.spec_from_file_location(str(file_path), file_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore

    for name_local in dir(module):
        if inspect.isclass(getattr(module, name_local)):
            return name_local


def get_algorithm_names(directory: str) -> dict[str, str]:
    algorithm_names: dict[str, str] = {}
    algorithms_directory = Path(__file__).parents[2] / "algorithms" / directory
    for i, algorithm_file in enumerate(algorithms_directory.glob("*.py")):
        algorithm_name = get_class_name_from(algorithm_file)
        if algorithm_name is not None:
            algorithm_names.update({str(algorithm_file): algorithm_name})
    return algorithm_names
