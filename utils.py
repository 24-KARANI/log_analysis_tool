import os

def load_log_file(path):
    """Load a log file and return its lines."""

    if not os.path.exists(path):
        raise FileNotFoundError(f"Log file not found at: {path}")
    
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    return lines