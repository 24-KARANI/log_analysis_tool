import re
from utils import load_log_file
from collections import deque

PACMAN_LOG_PATH = "/var/log/pacman.log"

def load_pacman_logs(limit=100):
    """Load the last `limit` lines of pacman.log and parse them."""
    parsed_entries = []

    try:
        with open(PACMAN_LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
            # keep only the last `limit` lines in memory
            last_lines = deque(f, maxlen=limit)

        for line in last_lines:
            parsed = parse_pacman_logs(line.strip())
            if parsed:
                parsed_entries.append(parsed)

    except FileNotFoundError:
        print(f"Pacman log not found at {PACMAN_LOG_PATH}")
    
    return parsed_entries


def parse_pacman_logs(line):
    """Parse pacman.log line into structured fields."""
    pattern = r"^\[(.*?)\]\s+\[(.*?)\]\s+(.*)$" 
    match = re.match(pattern, line)

    if not match:
        return None
    
    return {
        "timestamp": match.group(1),
        "action": match.group(2),
        "message": match.group(3)
    }