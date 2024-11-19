from abc import ABC, abstractmethod
from typing import Any, Sequence


class PreprocessEdge(ABC):
    """
    Meant for manually creating a tuple/dictionary/sequence if the data has no standardized format like csv or mtx
    Indicates the methods required for preprocessing the data.

    ...

    Methods
    -------
    create_edge_from(line)
        crates or modifies a python object (e.g. dictionary) from one line in the given dataset
    set_number_of_headers_to_ignore(lines_to_ignore)
        returns the result of the streaming algorithm once the whole dataset has been processed
    """

    @abstractmethod
    def create_edge_from(self, line: Any) -> Sequence | dict:
        """
        Creates a tuple from one line row from the parsed dataset.

        Parameters
        ----------
        line: Any
            Dataset row which could be any datatype depending on the format of the base file (e.g. string for .txt but dictionary for .csv)

        Returns
        -------
        Processed data row converted into a tuple
        """
        ...

    @abstractmethod
    def set_number_of_headers_to_ignore(self, lines_to_ignore: int = 1) -> None:
        """
        Sets the number of header lines in the base data file to ignore.

        Parameters
        ----------
        lines_to_ignore: int
            Number of first lines to omit
        """
        ...
