import pandas as pd

from algorithms._config.interfaces import BatchAlgorithm, ResultList


# Change this class name to something unique and descriptive
class NewBatchAlgorithm(BatchAlgorithm):
    def __init__(self) -> None:
        ...

    def calculate_property(self, data: pd.DataFrame) -> None:
        ...

    def submit_results(self) -> ResultList:
        ...
