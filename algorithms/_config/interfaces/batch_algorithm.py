from abc import ABC, abstractmethod
from typing import Any

import pandas as pd

numeric = int | float


class BatchAlgorithm(ABC):
    """
    Indicates the methods required for a streaming algorithm.

    ...

    Methods
    -------
    perform_calculations(data)
        Calculates the examined property of the data using batch processing for the purpose of verifying accuracy of the streaming algorithm
    submit_results()
        Returns the result of the batch algorithm in the form of a node rank
    """

    @abstractmethod
    def calculate_property(self, data: pd.DataFrame) -> None:
        """
        Calculates the examined property of the data using batch processing for the purpose of verifying accuracy of the streaming algorithm.
        Suggested usage of the networkx package.

        Parameters
        ----------
        data: pandas.DataFrame
            Dataset in the form of a pandas DataFrame

        Returns
        -------
        Result in the form of a node rank - a list of a number of nodes each with a numerical value
        indicating the calculated property of the node.
        """
        ...

    @abstractmethod
    def submit_results(self) -> list[tuple[Any, numeric]]:
        """
        Returns the result of the batch algorithm in the form of a node rank.

        Returns
        -------
        Result in the form of a node rank - a list of a number of nodes each with a numerical value
        indicating the calculated property of the node.
        """
        ...
