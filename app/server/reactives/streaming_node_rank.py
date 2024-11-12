import pandas as pd
from shiny import reactive, render

from .run_experiment import results


def server_streaming_node_rank():
    @reactive.calc
    def streaming_node_rank():
        streaming_results, *_ = results.get()
        df = pd.DataFrame(streaming_results, columns=["node", "value"])
        return df.head(20)

    @render.data_frame
    def render_streaming_node_rank():
        return render.DataGrid(streaming_node_rank())
