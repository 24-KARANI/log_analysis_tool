import os
import json
import glob
import hashlib
import pymongo
from pymongo import MongoClient, errors
from datetime import datetime

from parsers.pacman import load_pacman_logs
from parsers.journal import load_journal_logs
from parsers.audit import load_audit_logs
from parsers.login import load_login_sessions

from classification import classify_event
from aggregation import aggregate_statistics

RESULTS_DIR = "results"
MAX_RUNS = 5 

def rotate_results():
    """Keep only the last MAX_RUNS classified/stats pairs in results/."""
    files = sorted(
        glob.glob(os.path.join(RESULTS_DIR, "*.json")),
        key=os.path.getmtime
    )

    # Each run creates 2 files (classified + stats)
    max_files = MAX_RUNS * 2
    if len(files) > max_files:
        old_files = files[:len(files) - max_files]
        for f in old_files:
            try:
                os.remove(f)
                print(f"Removed old result file: {f}")
            except Exception as e:
                print(f"Could not remove {f}: {e}")

def make_id(entry):
    """
    Create a unique hash for a log entry based on its content.
    """
    raw = str(sorted(entry.items()))  # stable representation
    return hashlib.sha1(raw.encode()).hexdigest()


def save_to_mongodb(classified_entries, stats):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["log_analyzer"]

    timestamp = datetime.now()

    # --- Save classified entries with deduplication ---
    for entry in classified_entries:
        entry["_id"] = make_id(entry)   # ensure unique identifier
        entry["batch_timestamp"] = timestamp  # tag which run added it
        try:
            db.classified.insert_one(entry)
        except errors.DuplicateKeyError:
            # already stored → skip
            continue

    # --- Save aggregated stats as a single document ---
    db.stats.insert_one({
        "timestamp": timestamp,
        "stats": stats
    })

    print("Saved logs and stats to MongoDB (duplicates skipped).")

def main():
    classified_entries = []

    # --- PACMAN logs ---
    for entry in load_pacman_logs():
        classified = classify_event(entry, "pacman")
        if classified:
            classified_entries.append(classified)

    # --- JOURNAL logs ---
    for entry in load_journal_logs(limit=None, since="1 week ago"):
        classified = classify_event(entry, "journal")
        if classified:
            classified_entries.append(classified)

    # --- AUDIT logs ---
    for entry in load_audit_logs():
        classified = classify_event(entry, "audit")
        if classified:
            classified_entries.append(classified)

    # --- LOGIN sessions ---
    for entry in load_login_sessions():
        classified = classify_event(entry, "login")
        if classified:
            classified_entries.append(classified)

    os.makedirs("results", exist_ok=True)
    
    # --- Timestamped filenames ---
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    classified_path = os.path.join(RESULTS_DIR,f"classified_{timestamp}.json")
    stats_path = os.path.join(RESULTS_DIR,f"stats_{timestamp}.json")

    with open(classified_path, "w") as f:
        json.dump(classified_entries, f, indent=4)
    print(f"Classified events saved to {classified_path}")

    stats = aggregate_statistics(classified_entries)
    save_to_mongodb(classified_entries, stats)

    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=4)
    print(f"Aggregated statistics saved to {stats_path}")

    rotate_results()


if __name__ == "__main__":
    main()
    