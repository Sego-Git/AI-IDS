# Purpose: convert raw log lines (text) into simple numerci features for ML

import re  #re stand for regular expression(patter matching)
from pathlib import Path
import pandas as pd

IP_RE = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}")

def extract_features_from_line(line: str) -> dict:
    """ 
    Turn a single log line (string) into a small dict of numeric features.
    Each returned key is a feature column name."""
    
    # Defensive: if caller passes None, treat as empty string
    if line is None:
        line = ""
        
    length = len(line)    #'len': total characters in the line
    
    
    digits = sum(c.isdigit() for c in line)  # 'digits': count digit characters
    
   
    num_ips = len(IP_RE.findall(line)) # 'num_ips': how many IP-like tokens the regex finds (0,1,2,...)
    
    lower = line.lower()  # 'lower': count lowercase characters
    
    num_failed = lower.count("failed")
    
    num_auth = lower.count("auth")
    
    # Return a dict of the features (one row for a DataFrame)
    return {
        "len" : length,
        "digits": digits,
        "num_ips": num_ips,
        "num_failed": num_failed,
        "num_auth": num_auth,
    }
    
def lines_to_features(lines, out_csv: str=None):
    """
    convert an iterable of log lines into a pandas dataframe of features.
    If out_csv is provided, save the dataframe to CSV at that path.
    
    """
    
    # Build a list of feature dicts (one per line) using the extractor above
    rows = [extract_features_from_line(l) for l in lines]
    
    # Create a DataFrame (tabular representation) from the list of dicts
    df = pd.DataFrame(rows)
    
    # Optionally save CSV; create parent folders if needed
    if out_csv:
        out_path = Path(out_csv)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_path, index=False)
    # Return the DataFrame so callers can inspect or pass it to training
    return df

    

    