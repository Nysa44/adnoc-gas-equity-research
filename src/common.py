from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def load_assumptions(path=None):
    path = path or ROOT / "data" / "dcf_assumptions.csv"
    df = pd.read_csv(path)
    return {row["assumption"]: float(row["value"]) for _, row in df.iterrows()}
