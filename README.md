Log Analyzer

A Python-based tool for parsing, classifying, and aggregating Linux system logs.
The project is designed to help users monitor system activity by collecting logs from multiple sources, classifying events (e.g., package installs, sudo usage, login attempts), and storing results locally or in a MongoDB database.

✨ Features

Log Parsers:

Pacman logs → Tracks package installs

Journalctl logs → Tracks sudo usage and system errors

Audit logs → Tracks login attempts, authentication events, and access violations

Login sessions → Tracks user logins (from who and last)

Classification: Each log entry is classified into categories like package_install, sudo_usage, system_error, auth_event, etc.

Aggregation: Aggregates classified logs into meaningful statistics (e.g., installs per package, sudo usage per user).

Storage Options:

Save structured JSON results into a results/ folder

Insert logs into a local MongoDB database with duplicate prevention

Automation: Can be scheduled to run weekly via cron or systemd timer.

📂 Project Structure
log_analyzer/
├── analyze.py          # Main entry point
├── utils.py            # Shared utility functions
├── classification.py   # Event classification logic
├── aggregation.py      # Aggregation of statistics
├── parsers/            # Individual log parsers
│   ├── pacman.py
│   ├── journal.py
│   ├── audit.py
│   └── login.py
├── results/            # JSON output files (created at runtime)
└── README.md

⚡ Requirements

Linux (tested on Arch Linux, but adaptable to other distros)

Python 3.8+

MongoDB (optional, for database storage)

Python Dependencies

Install via pip:

pip install -r requirements.txt


Typical dependencies include:

pymongo

dnspython (if using MongoDB Atlas)

🚀 Usage
1. Clone Repository
git clone https://github.com/yourusername/log_analyzer.git
cd log_analyzer

2. Run Analyzer

Run locally (no DB):

python analyze.py


Run with MongoDB storage:

python analyze.py --db

3. Output

Classified logs and aggregated statistics are saved to JSON in the results/ folder:

results/
├── classified_2025-08-19_19-45-12.json
└── stats_2025-08-19_19-45-12.json


If MongoDB is enabled, entries are inserted into the logs database, events collection.

🔄 Automating Weekly Runs

You can automate weekly execution with cron:

crontab -e


Add:

0 0 * * 0 /path/to/venv/bin/python /path/to/log_analyzer/analyze.py


This runs every Sunday at midnight.

Or with systemd timers for more flexibility.

🧩 Future Enhancements

Email or Slack alerts for critical log events

Web dashboard for log visualization

Support for additional log sources (nginx, sshd, etc.)

⚠️ Notes

Some logs (e.g., /var/log/audit/audit.log) require root permissions. Run with:

sudo /path/to/venv/bin/python analyze.py


To avoid sudo, you can adjust log file permissions for your user.
