import subprocess

def collect_login_sessions():
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

def load_login_sessions():
    """Load and parse login sessions into stuctured fields"""

    login_entries = []

    parsed = collect_login_sessions()
    if parsed:
        login_entries.extend(parsed)

    return login_entries