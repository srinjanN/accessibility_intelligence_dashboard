"""
Decommission Local SQLite Database
Archives existing history.db to database/backups/ and safely deletes it.
"""

import os
import sys
import json
import shutil
import sqlite3
from datetime import datetime

# Ensure safe output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "database", "history.db")
BACKUP_DIR = os.path.join(PROJECT_ROOT, "database", "backups")

def main():
    print("=" * 70)
    print("[LOCAL DATABASE DECOMMISSIONING TOOL]")
    print("=" * 70)

    if not os.path.exists(DB_PATH):
        print(f"[*] Local database file '{DB_PATH}' does not exist or was already deleted.")
        print("[OK] Your dashboard is running exclusively in Cloud Mode on Supabase.")
        return

    # Check number of records in local database
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM analyses")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"[*] Local database currently contains {count} record(s).")
    except Exception as e:
        count = 0
        print(f"[!] Notice reading database: {e}")

    # Create safety backup before deletion
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_db = os.path.join(BACKUP_DIR, f"history_archived_{ts}.db")
    shutil.copy2(DB_PATH, backup_db)
    print(f"[+] Safety archive created at: {backup_db}")

    # Remove the file
    try:
        os.remove(DB_PATH)
        print(f"[OK] Local database '{DB_PATH}' successfully removed!")
        print("[OK] Local database dependency is completely eliminated.")
        print("     The dashboard now saves and loads history directly from Supabase.")
    except Exception as e:
        print(f"[!] Failed to delete file: {e}")
        print("    You may manually delete: " + DB_PATH)

if __name__ == "__main__":
    main()
