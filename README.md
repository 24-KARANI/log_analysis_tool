# 📊 Log Analysis Tool
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-5.0%2B-green)

A powerful Python tool for parsing, classifying, and aggregating Linux system logs. This tool provides a comprehensive overview of system activity by collecting logs from multiple sources, classifying events into structured categories, and storing the results locally or in a MongoDB database.

---

### ✨ Features

#### 🔍 Log Parsers
The tool includes dedicated parsers for a variety of critical system logs:
- **`pacman.log`**: Tracks package installations and removals.
- **`journalctl`**: Monitors `sudo` command usage and system-level errors from the systemd journal.
- **`audit.log`**: Records security-relevant events like login attempts, authentication successes/failures, and access control violations.
- **`who` & `last`**: Gathers information on current and historical user login sessions.

#### 🏷️ Event Classification
Each parsed log entry is intelligently categorized for easy filtering and analysis. Key categories include:
- `package_install`
- `package_removals`
- `sudo_usage`
- `system_error`
- `login_attempt`
- `auth_event`
- `access_violation`
- `user_login`

#### 📈 Statistics Aggregation
Generate meaningful summaries from the classified logs to identify trends and anomalies:
- **Sudo Usage**: Count of `sudo` commands executed per user.
- **Package Management**: Frequency of package installations and removals.
- **Login Activity**: Number of login attempts and successful logins per user.
- **System Errors**: Tally of errors grouped by the generating process (e.g., `kernel`, `systemd`).
- **Security Events**: Count of authentication events and access violations.

#### 💾 Flexible Storage
- **Local Files**: All classified logs and aggregated statistics are saved as timestamped JSON files in the `results/` directory.
- **MongoDB Integration**: Store structured log data in a MongoDB collection, with duplicate prevention based on entry content to ensure data integrity.

---

### 📂 Project Structure
```text
log_analysis_tool/
├── analyze.py          # Main script to run the log collection and analysis
├── classification.py   # Logic for categorizing log entries
├── aggregation.py      # Functions for aggregating statistics
├── utils.py            # Utility functions like file loading
├── parsers/              # Directory for individual log parsers
│   ├── audit.py
│   ├── journal.py
│   ├── login.py
│   └── pacman.py
└── README.md
```

---

### ⚙️ Requirements
- **System**: Linux (tested on Arch Linux)
- **Python**: 3.8+
- **Database**: MongoDB (Required for storing results)
- **Python Dependencies**:
  - `pymongo`

Install the required Python package using pip:
```bash
pip install pymongo
```

### 🚀 Quick Start

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/24-karani/log_analysis_tool.git
    cd log_analysis_tool
    ```

2.  **Run the Analyzer**
    Execute the main script. Ensure your MongoDB instance is running.
    ```bash
    python analyze.py
    ```
    > **Note**: Some log files (e.g., `/var/log/audit/audit.log`) require root privileges to read. You may need to run the script with `sudo`:
    > ```bash
    > sudo python analyze.py
    > ```

3.  **Review the Output**
    -   **Local JSON Files**: Check the `results/` directory for timestamped files containing the classified logs and aggregated statistics.
    ```text
    results/
    ├── classified_2023-10-27_10-30-00.json
    └── stats_2023-10-27_10-30-00.json
    ```
    -   **MongoDB**: The script inserts data into the `log_analyzer` database.
        -   Classified events are stored in the `classified` collection.
        -   Aggregated statistics are stored in the `stats` collection.

---

### 🔄 Automation with Cron

To run the analysis automatically (e.g., weekly), you can set up a cron job.

1.  Open your crontab for editing:
    ```bash
    sudo crontab -e
    ```

2.  Add the following line to execute the script every Sunday at 2:00 AM. Adjust the paths to your Python executable and the `analyze.py` script.
    ```
    0 2 * * 0 /usr/bin/python /path/to/log_analysis_tool/analyze.py
    ```

---

### 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or find any bugs, please feel free to open an issue or submit a pull request.

### 📄 License

This project is licensed under the MIT License.
