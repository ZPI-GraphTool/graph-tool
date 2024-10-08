from pathlib import Path

import pandas as pd

CONFIG_DIR = Path(__file__).resolve().parents[0]
STATIC_DIR = Path(__file__).resolve().parents[2] / "static"

STYLES_CSS_FILE = STATIC_DIR / "styles.css"
TIPS_CSV_FILE = STATIC_DIR / "tips.csv"

tips = pd.read_csv(TIPS_CSV_FILE)
