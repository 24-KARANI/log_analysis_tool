import subprocess
import re

def get_journal_logs(limit=None, since=None):
    """Get Get journalctl logs using subprocess."""

    cmd = ["journalctl", "--no-pager"]

    if limit:
        cmd.extend([f"-n{limit}"])
    if since:
        cmd.extend(["--since", since])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print("Error running journalctl:", e)
        return []

def parse_journal_log(line):
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

def load_journal_logs(limit, since):
    """Load and parse journalctl output into structured fields"""
    
    journal_logs = get_journal_logs(limit=limit, since=since)
    journal_entries = []

    print("\n=== JOURNAL LOGS (parsed) ===")
    for line in journal_logs:
        parsed = parse_journal_log(line)
        if parsed:
            journal_entries.append(parsed)

    return journal_entries
