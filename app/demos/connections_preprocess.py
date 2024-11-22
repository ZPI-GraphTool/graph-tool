from server.logic.interfaces import PreprocessEdge


class ConnectionPreprocess(PreprocessEdge):
    def create_edge_from(self, line):
        
        return (line["start_stop"], line["end_stop"])


