import json
from pathlib import Path
CONFIG_PATH = Path(__file__).parent / "config" / "config.json"

def load_config():
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"keywords": ["attack","suspicious","failed password"], "use_regex": False}
    
cfg = load_config()
SUSPICIOUS_KEYWORDS = cfg.get("keywords", [])
USE_REGEX = cfg.get("use_regex", False)


    