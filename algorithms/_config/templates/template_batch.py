from typing import Any

import pandas as pd

from algorithms._config.interfaces import BatchAlgorithm, numeric


# Change this class name to something unique and descriptive
class NewBatchAlgorithm(BatchAlgorithm):
    def __init__(self) -> None: 
        ...

    def calculate_property(self, data: pd.DataFrame) -> None: 
        ...

    def submit_results(self) -> list[tuple[Any, numeric]]: 
        ...
