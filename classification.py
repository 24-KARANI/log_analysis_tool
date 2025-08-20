def classify_event(entry, source):
    """
    Classify a parsed log entry into specific categories depending on source.
    """
    if not entry:
        return None

    category = None

    if source == "pacman":
        msg = entry.get("message", "").lower()
        if "installed" in msg :
            category = "package_install"
        elif "removed" in msg:
            category = "package_removals"

    elif source == "journal":
        msg = entry.get("message", "").lower()
        proc = entry.get("process", "").lower()
        if proc == "sudo" and "uid-0" in msg:
            category = "sudo_usage"
        elif proc in ("kernel", "systemd", "networkmanager", "unix_chkpwd"):
            if "error" in msg or "failed" in msg:
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