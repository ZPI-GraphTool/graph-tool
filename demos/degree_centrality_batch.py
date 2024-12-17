import networkx as nx
import pandas as pd

from algorithms._config.interfaces import BatchAlgorithm, ResultList


class DegreeCentralityBatch(BatchAlgorithm):
    def __init__(self) -> None:
        self.results = {}

    def calculate_property(self, data: pd.DataFrame) -> None:
        graph = nx.from_pandas_edgelist(  # type: ignore
            data,
            source=0,
            target=1,
            edge_attr=None,
            create_using=nx.MultiDiGraph(),  # type: ignore
        )
        self.results = nx.degree_centrality(graph)

    def submit_results(self) -> ResultList:
        return list(self.results.items())
