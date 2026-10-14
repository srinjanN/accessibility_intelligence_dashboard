"""
Migration Script: Local SQLite -> Supabase Cloud Database
Usage:
    python scripts/migrate_to_supabase.py
    python scripts/migrate_to_supabase.py --delete-local
    python scripts/migrate_to_supabase.py --dry-run
"""

import os
import sys
import json
import sqlite3
import argparse
from datetime import datetime

# Ensure safe output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

DB_PATH = os.path.join(PROJECT_ROOT, "database", "history.db")
BACKUP_DIR = os.path.join(PROJECT_ROOT, "database", "backups")

def get_supabase_client():
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_KEY", "").strip() or os.getenv("SUPABASE_ANON_KEY", "").strip()
    
    # Clean URL if it has /rest/v1
    if url.endswith("/rest/v1"):
        url = url[:-8]
    url = url.rstrip("/")
    
    if not url or not key:
        print("[!] Error: SUPABASE_URL and SUPABASE_KEY must be set in .env")
        print("    Current URL:", url or "(not set)")
        print("    Current KEY:", (key[:8] + "...") if key else "(not set)")
        sys.exit(1)
        
    try:
        from supabase import create_client
        return create_client(url, key)
    except ImportError:
        print("[!] Error: 'supabase' package is not installed. Run: pip install supabase")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error initializing Supabase client: {e}")
        sys.exit(1)

def check_supabase_table(client):
    """Check if 'analyses' table is ready in Supabase."""
    try:
        res = client.table("analyses").select("id").limit(1).execute()
        return True, "Table 'analyses' is active and accessible."
    except Exception as e:
        err = str(e)
        if "PGRST205" in err or "schema cache" in err or "relation" in err:
            return False, (
                "Table 'public.analyses' does not exist yet in your Supabase project.\n"
                "-> Please run 'scripts/schema_supabase.sql' in your Supabase SQL Editor:\n"
                f"   https://supabase.com/dashboard/project/{os.getenv('SUPABASE_PROJECT_REF', 'YOUR_PROJECT')}/sql"
            )
        return False, f"Supabase API notice: {err}"

def read_local_sqlite_records():
    """Read all records from local SQLite history.db."""
    if not os.path.exists(DB_PATH):
        print(f"[*] Local database file not found at: {DB_PATH}")
        return []
        
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM analyses ORDER BY id ASC")
        rows = cursor.fetchall()
        records = [dict(r) for r in rows]
        conn.close()
        return records
    except sqlite3.OperationalError as e:
        print(f"[!] Could not read analyses table from SQLite: {e}")
        conn.close()
        return []

def backup_sqlite_records(records):
    """Save JSON and SQLite backup files."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. JSON Backup
    json_path = os.path.join(BACKUP_DIR, f"history_backup_{timestamp}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
        
    # 2. SQLite File Copy
    if os.path.exists(DB_PATH):
        import shutil
        db_backup_path = os.path.join(BACKUP_DIR, f"history_backup_{timestamp}.db")
        shutil.copy2(DB_PATH, db_backup_path)
        
    print(f"[+] Safety backup created:")
    print(f"    -> JSON: {json_path}")
    if os.path.exists(DB_PATH):
        print(f"    -> DB:   {db_backup_path}")
    return json_path

def delete_local_sqlite():
    """Safely decommission local SQLite database."""
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print(f"[+] Successfully deleted local database: {DB_PATH}")
            return True
        except Exception as e:
            print(f"[!] Could not delete local database ({e}). You may delete it manually.")
            return False
    else:
        print(f"[*] Local database already deleted or does not exist.")
        return True

def main():
    parser = argparse.ArgumentParser(description="Migrate local SQLite history to Supabase cloud.")
    parser.add_argument("--delete-local", action="store_true", help="Delete local SQLite database after successful migration")
    parser.add_argument("--dry-run", action="store_true", help="Simulate migration without modifying Supabase or SQLite")
    parser.add_argument("--backup-only", action="store_true", help="Only create local backup without migrating")
    args = parser.parse_args()

    print("=" * 70)
    print("[SUPABASE CLOUD MIGRATION UTILITY]")
    print("=" * 70)

    # 1. Connect to Supabase
    print("\n[Step 1/4] Connecting to Supabase...")
    client = get_supabase_client()
    url = os.getenv("SUPABASE_URL", "")
    print(f"   Connected to Supabase endpoint: {url}")

    # 2. Check Supabase Table
    print("\n[Step 2/4] Verifying Supabase Table Schema...")
    table_ok, table_msg = check_supabase_table(client)
    if not table_ok:
        print(f"[!] {table_msg}")
        print("\nNext action needed:")
        print("1. Open your Supabase SQL Editor: https://supabase.com/dashboard")
        print("2. Paste and run 'scripts/schema_supabase.sql'")
        print("3. Re-run this script: python scripts/migrate_to_supabase.py")
        sys.exit(1)
    print(f"   [OK] {table_msg}")

    # 3. Read Local SQLite Records
    print("\n[Step 3/4] Reading Local SQLite Records...")
    records = read_local_sqlite_records()
    print(f"   Found {len(records)} record(s) in local SQLite database.")

    if not records:
        print("   [*] No records to migrate. Your Supabase database is ready for new records!")
        if args.delete_local:
            delete_local_sqlite()
        print("\n[OK] Migration process completed!")
        return

    # Always create backup before migrating
    print("\n[Backup] Creating local backup of existing records...")
    backup_sqlite_records(records)

    if args.backup_only:
        print("   [OK] Backup-only requested. Exiting.")
        return

    if args.dry_run:
        print("\n[Dry Run] Dry-run enabled. Skipping inserts.")
        print(f"   Would insert {len(records)} records into Supabase.")
        return

    # 4. Insert Records into Supabase
    print("\n[Step 4/4] Inserting Records into Supabase Cloud...")
    migrated_count = 0
    errors = 0

    payload_batch = []
    for r in records:
        row_payload = {
            "timestamp": r.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "doc_name": r.get("doc_name", "Untitled Copy"),
            "file_type": r.get("file_type", "Pasted Text"),
            "input_text": r.get("input_text", ""),
            "accessibility_score": float(r.get("accessibility_score", 0.0)),
            "readability_score": float(r.get("readability_score", 0.0)),
            "grade_level": float(r.get("grade_level", 0.0)),
            "reading_time": float(r.get("reading_time", 0.0)),
            "violations_count": int(r.get("violations_count", 0)),
            "issues_json": r.get("issues_json", "[]"),
            "metrics_json": r.get("metrics_json", "{}"),
            "simplified_text": r.get("simplified_text", "") or ""
        }
        payload_batch.append(row_payload)

    # Insert in batches of 50
    batch_size = 50
    for i in range(0, len(payload_batch), batch_size):
        chunk = payload_batch[i:i + batch_size]
        try:
            res = client.table("analyses").insert(chunk).execute()
            migrated_count += len(res.data) if res.data else len(chunk)
            print(f"   [+] Batch {i // batch_size + 1}: Migrated {len(chunk)} record(s)...")
        except Exception as e:
            print(f"   [!] Batch {i // batch_size + 1} failed: {e}")
            errors += len(chunk)

    print("\n" + "=" * 70)
    print(f"[MIGRATION SUMMARY]")
    print(f"   Total Local Records:    {len(records)}")
    print(f"   Migrated to Supabase:   {migrated_count}")
    print(f"   Failed:                 {errors}")
    print("=" * 70)

    # Verification in Supabase
    try:
        count_res = client.table("analyses").select("id", count="exact").execute()
        cloud_total = count_res.count if hasattr(count_res, "count") and count_res.count is not None else len(count_res.data)
        print(f"[*] Current Total Records in Supabase: {cloud_total}")
    except Exception:
        pass

    # 5. Delete Local Database if requested
    if args.delete_local and errors == 0:
        print("\n[Decommissioning] Deleting local SQLite database as requested...")
        delete_local_sqlite()
    elif not args.delete_local and errors == 0:
        print("\n[*] Local database was preserved. To safely delete it, run:")
        print("    python scripts/decommission_local_db.py")

    print("\n[OK] All operations complete! Your application now operates on Supabase.")

if __name__ == "__main__":
    main()
