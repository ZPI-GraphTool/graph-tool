from abc import ABC, abstractmethod
from typing import Tuple, Any, List, Union, TypeAlias
import pandas as pd

numeric: TypeAlias = Union[int, float]

class BatchAlgorithm(ABC):
    """
    Indicates the methods required for a streaming algorithm  

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
        Calculates the examined property of the data using batch processing for the purpose of verifying accuracy of the streaming algorithm
        Suggested usage of the networkx package

        Parameters
        ----------
        data: DataFrame 
            Dataset in the form of a pandas DataFrame 

        Returns
        -------
        Results in the form of a node rank - a list of a number of nodes each with a numerical value 
        indicating the calculated property of the node
        """
        pass

    

    @abstractmethod
    def submit_results(self) -> List[Tuple[Any, numeric]]:
        """
        Returns the result of the batch algorithm in the form of a node rank

        Returns
        -------
        Results in the form of a node rank - a list of a number of nodes each with a numerical value 
        indicating the calculated property of the node
        """
        pass



class PreprocessEdge(ABC):
    """
    Meant for manually creating a Tuple/Dictionary/Sequence if the data has no standardized format like csv or mtx
    Indicates the methods required for preprocessing the data. 

    ...

    Methods
    -------
    create_edge_from(line)
        crates a tuple from one line in the given dataset
    set_number_of_headers_to_ignore(lines_to_ignore)
        returns the result of the streaming algorithm once the whole dataset has been processed

    """

    @abstractmethod
    def create_edge_from(self, line: Any) -> Tuple[Any, ...]:
        """
        Creates a tuple from one line row from the parsed dataset

        Parameters
        ----------
        line: Any 
            Dataset row which could be any datatype depending on the format of the base file (e.g. string for .txt but dictionary for .csv)

        Returns
        -------
        Processed data row converted into a tuple
        """
        pass


    @abstractmethod
    def set_number_of_headers_to_ignore(self, lines_to_ignore: int = 1) -> None:
        """
        Sets the number of header lines in the base data file to ignore

        Parameters
        ----------
        lines_to_ignore: int 
            Number of first lines to omit
        """
        pass



numeric: TypeAlias = Union[int, float]

class StreamingAlgorithm(ABC):
    """
    Indicates the methods required for a streaming algorithm  

    ...

    Methods
    -------
    on_edge_calculate(edge)
        performs a set of instructions on one edge
    submit_results()
        returns the result of the streaming algorithm once the whole dataset has been processed

    """

    @abstractmethod
    def on_edge_calculate(self, edge: Tuple[Any, ...]) -> None:
        """
        Performs a set of instructions on one given edge

        Parameters
        ----------
        edge: tuple
            Edge in the form of a tuple 

        """
        pass
    

    @abstractmethod
    def submit_results(self) -> List[Tuple[Any, numeric]]:
        """
        Submits the result of the streaming algorithm - determines part of the results to be saved to file
        and displayed in the UI

        Returns
        -------
        Results in the form of a node rank - a list of a number of nodes each with a numerical value 
        indicating the calculated property of the node
        """
        pass
