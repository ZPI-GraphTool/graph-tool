from pathlib import Path

THIS = Path(__file__).resolve().parent

with open(THIS / "app" / "demos" / "connections.csv", encoding="cp1250") as f:
    print(f.read())
