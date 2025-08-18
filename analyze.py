import os
import re
import subprocess

def load_log_file(filepath):
    """Load a log file and return its lines."""

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"log file not found: {filepath}")
    
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    return lines

def parse_log_line(line):
    """Parse a pacman.log line into structured fields."""

    # Regex for pacman.log
    pattern = r"^\[(.*?)\]\s+\[(.*?)\]\s+(.*)$"
    match = re.match(pattern, line)

    if not match:
        return None
    
    return {
        "timestamp": match.group(1),
        "action": match.group(2),
        "message": match.group(3)
    }

def get_journal_logs(limit=50):
    """Get journalctl logs using subprocess."""

    try:
        result = subprocess.run(
            ["journalctl", f"-n{limit}", "--no-pager"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print("Error running journalctl:", e)
        return []
    
def parse_journal_line(line):
    """Parse a journalctl line into structured fields."""
    pattern = re.compile(
        r'^(?P<timestamp>\w{3} \d{2} \d{2}:\d{2}:\d{2}) '
        r'(?P<hostname>\w+) '
        r'(?P<process>\w+)(?:\[(?P<pid>\d+)\])?: '
        r'(?P<message>.*)$'
    )
    match = re.match(pattern, line)

    if not match:
        return None
    
    return {
        "timestamp": match.group("timestamp"),
        "hostname": match.group("hostname"),
        "process": match.group("process"),
        "pid": match.group("pid"),
        "message": match.group("message"),
    }


if __name__=="__main__":
    test_file = "/home/karani/Documents/projects/log_analyzer/test_logs.txt"
    logs = load_log_file(test_file)

    for line in logs[:5]:
        parsed = parse_log_line(line)
        print(parsed)

    # Test Journalctl 
    journal_logs = get_journal_logs(limit=10)
    for line in journal_logs:
        parsed = parse_journal_line(line)
        if parsed:
            print(parsed)