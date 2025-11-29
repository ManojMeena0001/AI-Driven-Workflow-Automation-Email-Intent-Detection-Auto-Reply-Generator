# src/predict.py
from src.utils import load_model_pipeline
from typing import Dict, Any, List
import numpy as np

DEFAULT_MODEL_PATH = "model/intent_pipeline.joblib"

class IntentPredictor:
    """A class to load the model and make intent predictions."""
    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        print(f"[INFO] Loading model from: {model_path}")
        self.pipeline = load_model_pipeline(model_path)
        # Extract class labels from the trained model
        self.classes_ = self.pipeline.named_steps['clf'].classes_

    def predict(self, text_list: List[str]) -> List[Dict[str, Any]]:
        """
        Runs the full pipeline (TF-IDF + Classifier) on a list of clean texts.
        Returns predicted intent, confidence, and scores for each text.
        """
        # 1. Predict probabilities
        probabilities = self.pipeline.predict_proba(text_list)
        
        results = []
        for proba in probabilities:
            # 2. Get the index of the highest probability
            top_idx = int(np.argmax(proba))
            
            # 3. Get the corresponding intent and confidence
            intent = self.classes_[top_idx]
            confidence = float(proba[top_idx])
            
            # 4. Build a dictionary of all scores (class: probability)
            scores = {c: float(p) for c, p in zip(self.classes_, proba)}
            
            results.append({
                "intent": intent, 
                "confidence": confidence, 
                "scores": scores
            })
            
        return results