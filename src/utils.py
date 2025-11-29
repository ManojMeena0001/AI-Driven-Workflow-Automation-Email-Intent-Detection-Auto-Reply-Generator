import pandas as pd                            # # Importing pandas library for data manipulation
from typing import Optional, Dict , Any                 # # Importing necessary types for type hinting
import os
import joblib


def load_raw_data(path: str) -> pd.DataFrame:
    """Load CSV data and ensures basic text columns are present."""
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"file not found at {path}")
        return pd.DataFrame()
# Concatenate subject and body into a single 'text' column for processing
    subj = df.get('subject', pd.Series([""]*len(df)))
    body = df.get('body', pd.Series([""]*len(df)))
    df['text'] = (subj.fillna('') + ' ' + body.fillna('')).astype(str).str.strip()
    return df

def ensure_dirs(dirs: list = ["data", "model", "logs"]):
    """Ensure necessary project directories exist."""
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print(f"[INFO] Ensured directories: {dirs}")

def load_model_pipeline(model_path: str) -> Any:
    """Load the trained joblib model pipeline."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model not found at {model_path}. Did you run the Colab notebook?")
    return joblib.load(model_path)