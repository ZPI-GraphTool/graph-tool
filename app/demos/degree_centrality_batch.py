import networkx as nx
from server.logic.interfaces import BatchAlgorithm


class DegreeCentralityBatch(BatchAlgorithm):
    def __init__(self):
        self.results = {}

    def calculate_property(self, data):
        graph_type = nx.MultiDiGraph()

        graph = nx.from_pandas_edgelist(
            data,
            source="start_stop",
            target="end_stop",
            edge_attr=None,
            create_using=graph_type,
        )
        self.results = nx.degree_centrality(graph)

    def submit_results(self):
        degree_centralities = sorted(
            self.results.items(), key=lambda item: item[1], reverse=True
        )

        return degree_centralities
