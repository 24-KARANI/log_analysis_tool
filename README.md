📊
log_analysis_tool
Python License

A powerful Python-based tool for parsing, classifying, and aggregating Linux system logs. Monitor your system activity by collecting logs from multiple sources, classifying events, and storing results locally or in MongoDB.

✨ Features
🔍 Log Parsers
Pacman logs → Tracks package installations and updates

Journalctl logs → Monitors sudo usage and system errors

Audit logs → Records login attempts, authentication events, and access violations

Login sessions → Tracks user logins (from who and last commands)

🏷️ Classification
Each log entry is intelligently categorized into:

package_install

sudo_usage

system_error

auth_event

And more...

📈 Aggregation
Generate meaningful statistics from your logs:

Installs per package

Sudo usage per user

Login attempts over time

System error frequency

💾 Storage Options
Save structured JSON results to local files

Insert into MongoDB with duplicate prevention

Flexible output formats

⚙️ Automation
Easily schedule weekly runs via:

cron jobs

systemd timers

📂 Project Structure
text
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
System
Linux (tested on Arch Linux, but adaptable to other distros)

Python 3.8+

MongoDB (optional, for database storage)

Python Dependencies
Install via pip:

bash
pip install -r requirements.txt
Typical dependencies include:

pymongo

dnspython (if using MongoDB Atlas)

🚀 Quick Start
1. Clone Repository
bash
git clone https://github.com/yourusername/log_analyzer.git
cd log_analyzer
2. Run the Analyzer
Run locally (no database):

bash
python analyze.py
Run with MongoDB storage:

bash
python analyze.py --db
3. Output
Classified logs and aggregated statistics are saved to JSON in the results/ folder:

text
results/
├── classified_2025-08-19_19-45-12.json
└── stats_2025-08-19_19-45-12.json
If MongoDB is enabled, entries are inserted into the logs database, events collection.

🔄 Automation
Cron Job (Weekly Execution)
bash
crontab -e
Add the following line to run every Sunday at midnight:

text
0 0 * * 0 /path/to/venv/bin/python /path/to/log_analyzer/analyze.py
Systemd Timer
For more flexibility and better logging, consider using systemd timers (configuration examples available in the wiki).

🛠️ Permissions Note
Some logs (e.g., /var/log/audit/audit.log) require root permissions. Run with:

bash
sudo /path/to/venv/bin/python analyze.py
Alternatively, adjust log file permissions for your user to avoid using sudo.

🧩 Future Enhancements
Email or Slack alerts for critical log events

Web dashboard for log visualization

Support for additional log sources (nginx, sshd, etc.)

Real-time log monitoring capabilities

Advanced filtering and search capabilities

🤝 Contributing
We welcome contributions! Please feel free to submit pull requests, open issues, or suggest new features.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
