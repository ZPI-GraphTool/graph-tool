
from streaming.interfaces import PreprocessEdge


class ConnectionPreprocess(PreprocessEdge):


    def create_edge_from(self, line):
        print("Called create edge")
        return ("","")
    
    # this does not make sense 
    def set_number_of_headers_to_ignore(self, lines_to_ignore = 1):
        return super().set_number_of_headers_to_ignore(lines_to_ignore)