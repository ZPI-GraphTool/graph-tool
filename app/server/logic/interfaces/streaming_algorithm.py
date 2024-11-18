from abc import ABC, abstractmethod
from typing import Any, Sequence

numeric = int | float


class StreamingAlgorithm(ABC):
    """
    Indicates the methods required for a streaming algorithm.

    ...

    Methods
    -------
    on_edge_calculate(edge)
        performs a set of instructions on one edge
    submit_results()
        returns the result of the streaming algorithm once the whole dataset has been processed
    """

    @abstractmethod
    def on_edge_calculate(self, edge: Sequence | dict) -> None:
        """
        Performs a set of instructions on one given edge.

        Parameters
        ----------
        edge: sequence or dictionary
            Edge in the form of a tuple

        """
        ...

    @abstractmethod
    def submit_results(self) -> list[tuple[Any, numeric]]:
        """
        Submits the result of the streaming algorithm - determines part of the results to be saved to file
        and displayed in the UI.

        Returns
        -------
        Results in the form of a node rank - a list of a number of nodes each with a numerical value
        indicating the calculated property of the node
        """
        ...
