import joblib
from sklearn.ensemble import IsolationForest
import pandas as pd
from pathlib import Path

MODEL_PATH = Path("models") / "isolation_forest.joblib"
MODEL_PATH.parent.mkdir(exist_ok=True)

def train_from_csv(feature_csv: str):
    """
    Train an Isolation Forest model from a CSV of features.
    Save the trained model to disk at MODEL_PATH.
    """
    # Load the CSV into a DataFrame
    df = pd.read_csv(feature_csv)
    
    # Train the Isolation Forest model
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(df)
    
    # Save the trained model to disk
    joblib.dump(model, MODEL_PATH)
    print(f"Model trained and saved to {MODEL_PATH}")
    
if __name__ == "__main__":
    #Allows: python src/train.py
    
    import sys
    from pathlib import Path
    
    csv = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/processed/features.csv")
    if not csv.exists():
        print("No features file found at", csv)
        raise SystemExit(1)
    train_from_csv(csv)
    