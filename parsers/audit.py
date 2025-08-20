import os
from utils import load_log_file

def parse_audit_line(line):
    """Parse an audit.log line into a dictionary of key-value pairs."""
    
    if not line.startswith("type="):
        return None
    
    audits = line.split()
    log_dict = {}

    for audit in audits:
        if "=" in audit:
            k, v = audit.split("=", 1)
            log_dict[k] = v.strip('"')

    return log_dict

def load_audit_logs(path="/var/log/audit/audit.log"):
    """Load and parse audit.log into structured entries."""
    
    audit_entries = []
    audit_logs = load_log_file(path)
    
    print("\n=== AUDIT LOGS (parsed) ===")   
    for line in audit_logs:
        parsed = parse_audit_line(line)
        if parsed:
            audit_entries.append(parsed)
    
    return audit_entries
