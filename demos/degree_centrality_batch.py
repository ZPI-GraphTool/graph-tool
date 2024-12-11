from typing import Any

import networkx as nx
import pandas as pd

from algorithms._config.interfaces import BatchAlgorithm, numeric


class DegreeCentralityBatch(BatchAlgorithm):
    def __init__(self) -> None:
        self.results = {}

    def calculate_property(self, data: pd.DataFrame) -> None:
        graph = nx.from_pandas_edgelist(  # type: ignore
            data,
            source="start_stop",
            target="end_stop",
            edge_attr=None,
            create_using=nx.MultiDiGraph(),  # type: ignore
        )
        self.results = nx.degree_centrality(graph)

    def submit_results(self) -> list[tuple[Any, numeric]]:
        return self.results.items()
