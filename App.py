from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import json
import threading
from pathlib import Path

from src.features import lines_to_features
from src.train import train_from_csv
from src.inference import load_model, predict_lines
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

MODEL_PATH = Path("models") / "isolation_forest.joblib"
SUSPICIOUS_KEYWORDS = ["attack", "suspicious", "failed password"]
#Add the background training helper

TRAINING_STATUS = {"running": False, "message": ""}

def model_ready():
    return MODEL_PATH.exists()

def _run_training_thread(features_csv: str):
    try:
        TRAINING_STATUS["running"] = True
        TRAINING_STATUS["message"] = "training..."
        train_from_csv(features_csv)
        TRAINING_STATUS["message"] = "training completed"
    except Exception as e:
        TRAINING_STATUS["message"] = f"training error: {e}"
    finally:
        TRAINING_STATUS["running"] = False

#add a complete index route (GET + POST) and status endpoint
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("log_file")
        if uploaded_file and uploaded_file.filename != "":
            raw_dir = Path("data") / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)
            filename = secure_filename(uploaded_file.filename)
            saved_path = raw_dir / filename
            uploaded_file.save(str(saved_path))

            text = saved_path.read_text(encoding="utf-8", errors="ignore")
            lines = [l.strip() for l in text.splitlines() if l.strip()]

            processed_dir = Path("data") / "processed"
            processed_dir.mkdir(parents=True, exist_ok=True)
            features_csv = processed_dir / "features.csv"
            lines_to_features(lines, out_csv=str(features_csv))

            if not TRAINING_STATUS["running"]:
                t = threading.Thread(
                    target=_run_training_thread,
                    args=(str(features_csv),),
                    daemon=True,
                )
                t.start()
                TRAINING_STATUS["message"] = "training started"
            else:
                TRAINING_STATUS["message"] = "training already running"

            if model_ready():
                model = load_model()
                results = predict_lines(model, lines)
                for item in results:
                    # inference returns 'anomaly' (boolean); map it to 'suspicious' for the template
                    item["suspicious"] = item.get("anomaly", False)
            else:
                results = []
                for line in lines:
                    suspicious = any(keyword in line.lower()  for keyword in SUSPICIOUS_KEYWORDS)
                    results.append({"line": line, "suspicious":suspicious})
                    
            suspicious_count = sum(1 for item in results if item["suspicious"])
            
            return render_template(
                "index.html",
                suspicious_count = suspicious_count,
                results = results,
                train_status = TRAINING_STATUS,
                model_ready = model_ready(),
                uploaded_filename = filename,
            )

    # GET request: just show the form with no results
    return render_template(
        "index.html",
        suspicious_count=0,
        results=[],
        train_status=TRAINING_STATUS,
        model_ready = model_ready(),
        uploaded_filename = None,
    )


@app.route("/train_status")
def train_status():
    return TRAINING_STATUS


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)