from pathlib import Path

DEMOS_DIR = Path(__file__).resolve().parents[0]

CONNECTIONS_CSV_FILE = DEMOS_DIR / "connections.csv"
CONNECTIONS_PREPROCESS_FUNCTION_FILE = DEMOS_DIR / "connections_preprocess.py"
DEGREE_CENTRALITY_BATCH_ALGORITHM_FILE = DEMOS_DIR / "degree_centrality_batch.py"
DEGREE_CENTRALITY_STREAM_ALGORITHM_FILE = DEMOS_DIR / "degree_centrality_stream.py"
