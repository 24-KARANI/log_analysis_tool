import os
import re
import subprocess
import shlex

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

def parse_audit_line(line):
    """Parse an audit.log line into a dictionary of key-value pairs."""
    
    if not line.startswith("type="):
        return None
    
    audits = line.split()
    log_dict = {}

    for audit in audits:
        if "=" in audit:
            k, v = audit.split("=", 1)
            log_dict[k] = v

    return log_dict

def parse_login_sessions():
    """Collect sessions from both 'who' (current) and 'last' (historical)"""
    sessions = []
    
    try:
        # Current sessions from 'who'
        result = subprocess.run(['who'], capture_output=True, text=True, check=True)
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split()
                if len(parts) >= 2:
                    sessions.append({
                        "username": parts[0],
                        "tty": parts[1],
                        "details": ' '.join(parts[2:]),  # everything else
                        "source": "who"
                    })
    except Exception as e:
        print(f"'who' failed: {e}")

    try:
        # Historical sessions from 'last'
        result = subprocess.run(['last'], capture_output=True, text=True, check=True)
        for line in result.stdout.strip().split('\n'):
            if line and not line.startswith('wtmp'):
                parts = line.split()
                if len(parts) >= 2:
                    sessions.append({
                        "username": parts[0],
                        "tty": parts[1],
                        "details": ' '.join(parts[2:]),  # everything else
                        "source": "last"
                    })
    except Exception as e:
        print(f"'last' failed: {e}")

    return sessions

def classify_event(entry, source):
    """
    Classify a parsed log entry into specific categories depending on source.
    """
    if not entry:
        return None

    category = None

    if source == "pacman":
        msg = entry.get("message", "").lower()
        if "installed" in msg or "pacman -s" in msg:
            category = "package_install"

    elif source == "journal":
        msg = entry.get("message", "").lower()
        proc = entry.get("process", "").lower()
        if proc == "sudo":
            category = "sudo_usage"
        elif "error" in msg or "failed" in msg:
            category = "system_error"

    elif source == "audit":
        t = entry.get("type")
        if t in ("USER_LOGIN", "USER_START"):
            category = "login_attempt"
        elif t in ("USER_AUTH", "CRED_REFR"):
            category = "auth_event"
        elif t == "AVC":
            category = "access_violation"
        elif t == "SYSCALL" and entry.get("comm") == '"sudo"':
            category = "auth_event" 

    elif source == "login":
        category = "user_login"

    if category:
        entry["category"] = category
        return entry
    return None

from collections import defaultdict, Counter

from collections import Counter

def aggregate_statistics(entries):
    """
    Aggregate log entries into meaningful statistics per category.
    Returns a dict of counters keyed by category.
    """
    stats = {
        "pacman_installs": Counter(),
        "sudo_usage": Counter(),
        "system_errors": Counter(),
        "audit_login_attempts": Counter(),
        "audit_auth_events": Counter(),
        "audit_access_violations": Counter(),
        "user_logins": Counter()
    }

    for e in entries:
        cat = e.get("category")

        # --- Pacman installs ---
        if cat == "package_install":
            msg = e.get("message", "")
            parts = msg.split()
            pkg = parts[1] if len(parts) > 1 else "unknown"
            stats["pacman_installs"][pkg] += 1

        # --- Journalctl sudo usage ---
        elif cat == "sudo_usage":
            # Try to extract user from message like "user karani executed command ..."
            msg = e.get("message", "")
            user = "unknown"
            for token in msg.split():
                if token.lower() == "user":
                    idx = msg.split().index(token)
                    if idx + 1 < len(msg.split()):
                        user = msg.split()[idx+1]
                        break
            stats["sudo_usage"][user] += 1

        # --- Journalctl system errors ---
        elif cat == "system_error":
            proc = e.get("process", "unknown")
            stats["system_errors"][proc] += 1

        # --- Audit login attempts ---
        elif cat == "login_attempt":
            user = e.get("AUID") or e.get("auid") or e.get("UID") or e.get("uid") or "unknown"
            stats["audit_login_attempts"][user] += 1

        # --- Audit authentication events ---
        elif cat == "auth_event":
            user = e.get("UID") or e.get("uid") or "unknown"
            stats["audit_auth_events"][user] += 1

        # --- Audit access violations ---
        elif cat == "access_violation":
            exe = e.get("exe") or "unknown"
            stats["audit_access_violations"][exe] += 1

        # --- Login sessions ---
        elif cat == "user_login":
            user = e.get("username") or e.get("user") or "unknown"
            stats["user_logins"][user] += 1

    return stats




if __name__ == "__main__":
    classified_entries = []

    # PACMAN
    pacman_file = "/var/log/pacman.log"
    logs = load_log_file(pacman_file)
    for line in logs[:20]:
        parsed = parse_log_line(line)
        classified = classify_event(parsed, "pacman")
        if classified:
            classified_entries.append(classified)

    # JOURNAL
    journal_logs = get_journal_logs(limit=20)
    for line in journal_logs:
        parsed = parse_journal_line(line)
        classified = classify_event(parsed, "journal")
        if classified:
            classified_entries.append(classified)

    # AUDIT
    audit_file = "/var/log/audit/audit.log"
    if os.path.exists(audit_file):
        audit_logs = load_log_file(audit_file)
        for line in audit_logs[:20]:
            parsed = parse_audit_line(line)
            classified = classify_event(parsed, "audit")
            if classified:
                classified_entries.append(classified)

    # LOGIN
    sessions = parse_login_sessions()
    for s in sessions[:10]:
        classified = classify_event(s, "login")
        if classified:
            classified_entries.append(classified)

    # === AGGREGATION ===
    stats = aggregate_statistics(classified_entries)

    print("\n=== Aggregated Statistics ===")
    for section, counts in stats.items():
        print(f"{section}: {dict(counts)}")

    