from collections import Counter

def aggregate_statistics(entries):
    """
    Aggregate log entries into meaningful statistics per category.
    Returns a dict of counters keyed by category.
    """
    stats = {
        "pacman_installs": Counter(),
        "pacman_removals": Counter(),
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
            pkg = parts[-2] if len(parts) > 1 else "unknown"
            stats["pacman_installs"][pkg] += 1

        # --- Pacman removals ---
        elif cat == "package_removals":
            msg = e.get("message", "")
            parts = msg.split()
            pkg = parts[-2] if len(parts) > 1 else "unknown"
            stats["pacman_removals"][pkg] += 1

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