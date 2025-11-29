# src/preprocess.py
import re
from typing import List

def clean_text_for_model(text: str) -> str:
    """
    Applies the exact cleaning steps needed for the model trained in Colab.
    
    IMPORTANT: We must match the training data preparation. Since the Colab demo 
    used raw strings, we perform only minimal cleaning here.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # Remove special characters and numbers (optional, but keeps model simple)
    # Since the Colab model was trained on simple, raw text, we keep the cleaning minimal
    text = re.sub(r'[^a-z\s]', '', text) 
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def prepare_text_column(df: pd.DataFrame, text_col: str = 'text') -> pd.DataFrame:
    """Apply cleaning to the designated text column."""
    df = df.copy()
    df['text_clean'] = df[text_col].fillna('').astype(str).apply(clean_text_for_model)
    return df