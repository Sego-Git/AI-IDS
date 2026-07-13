# src/inference.py
#Load and run the trained model

from pathlib import Path
from xml.parsers.expat import model
import joblib
import pandas as pd

#Import the feature extractor 

from src.features import extract_features_from_line

#Location where training saves the model
MODEL_PATH = Path("models") / "isolation_forest.joblib"

def load_model():
    """
    Return loaded model or None if nt found."""
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None

def predict_lines(model, lines):
    
    """ Given a loaded model and iterable of text linesm return a list of dicts:
    { 
    'line':str, 'score':float, 'pred': int, 'anomaly': bool
    - 'Score' is the model's decision funtion (higher = more normal for IsolationForest)
    - 'pred' is model.predict output (1 normal, -1 anomaly)
    'anomaly' is True when pred == -1}"""
    
    if model is None:
        return None 
  # Build features DataFrame from lines(call the small extractor per line)
    feats = pd.DataFrame([extract_features_from_line(l) for l in lines])
  #Model outputs: decision_function(continuous  & predict (1 or -1))
    scores = model.decision_function(feats)
    preds = model.predict(feats)

    results = []
    for line, s, p in zip(lines, scores, preds):
        results.append({
            'line': line,
            'score': float(s),
            'pred': int(p),
            'anomaly': bool(p == -1),
        })
    return results