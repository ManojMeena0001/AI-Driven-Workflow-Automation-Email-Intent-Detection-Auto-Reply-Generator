import re
from typing import List
import pandas as pd


def clean_text_for_model(text: str) -> str:
    """
    Simple cleaning used by the training pipeline: lowercase, remove non-alpha chars,
    collapse whitespace.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def prepare_text_column(df: pd.DataFrame, text_col: str = 'text') -> pd.DataFrame:
    """Apply cleaning to the designated text column and return new DataFrame.

    Adds a new column `text_clean` expected by the rest of the pipeline.
    """
    df = df.copy()
    df['text_clean'] = df[text_col].fillna('').astype(str).apply(clean_text_for_model)
    return df
