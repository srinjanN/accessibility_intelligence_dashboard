"""
Automated Supabase SQL Execution Script.
Executes schema_supabase.sql directly on Supabase via:
1. Supabase Management API (using Personal Access Token: sbp_...)
   OR
2. Direct PostgreSQL connection (using database password)
"""

import os
import sys
import argparse
import requests

# Ensure safe output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

SCHEMA_PATH = os.path.join(PROJECT_ROOT, "scripts", "schema_supabase.sql")
PROJECT_REF = os.getenv("SUPABASE_PROJECT_REF", "frkbjkugjfbvufsszxjm")

def execute_via_management_api(token: str, sql_query: str) -> bool:
    """Execute SQL query via Supabase Management API."""
    url = f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query"
    headers = {
        "Authorization": f"Bearer {token.strip()}",
        "Content-Type": "application/json"
    }
    print(f"[*] Sending SQL execution request to Supabase Management API...")
    print(f"    Target Project: {PROJECT_REF}")
    
    try:
        response = requests.post(url, headers=headers, json={"query": sql_query}, timeout=30)
        if response.status_code == 200 or response.status_code == 201:
            print("[OK] SQL executed successfully in Supabase!")
            return True
        else:
            print(f"[!] Management API error (Status {response.status_code}): {response.text}")
            return False
    except Exception as e:
        print(f"[!] Failed to call Supabase Management API: {e}")
        return False

def execute_via_postgres(password: str, sql_query: str) -> bool:
    """Execute SQL query via direct PostgreSQL connection."""
    import psycopg
    conn_str = f"postgresql://postgres:{password}@db.{PROJECT_REF}.supabase.co:5432/postgres?sslmode=require"
    print(f"[*] Connecting directly to Supabase PostgreSQL at db.{PROJECT_REF}.supabase.co:5432...")
    
    try:
        with psycopg.connect(conn_str, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_query)
        print("[OK] SQL executed successfully via direct PostgreSQL connection!")
        return True
    except Exception as e:
        print(f"[!] Direct connection failed: {e}")
        # Try session pooler on port 6543
        print("[*] Retrying via Supabase transaction pooler (port 6543)...")
        pooler_str = f"postgresql://postgres.{PROJECT_REF}:{password}@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require"
        try:
            with psycopg.connect(pooler_str, autocommit=True) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql_query)
            print("[OK] SQL executed successfully via pooler connection!")
            return True
        except Exception as e2:
            print(f"[!] Pooler connection failed: {e2}")
            return False

def verify_table_ready() -> bool:
    """Verify that table 'analyses' is now visible to Supabase Data API."""
    url = os.getenv("SUPABASE_URL", f"https://{PROJECT_REF}.supabase.co")
    key = os.getenv("SUPABASE_KEY", "") or os.getenv("SUPABASE_ANON_KEY", "")
    
    # Clean URL
    if url.endswith("/rest/v1"):
        url = url[:-8]
    url = url.rstrip("/")
    
    try:
        from supabase import create_client
        client = create_client(url, key)
        res = client.table("analyses").select("id").limit(1).execute()
        print(f"[OK] Table 'analyses' is verified and live on Supabase Data API! (Found {len(res.data)} sample records)")
        return True
    except Exception as e:
        print(f"[!] Verification notice: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Execute Supabase SQL schema automatically.")
    parser.add_argument("--token", help="Supabase Personal Access Token (from https://supabase.com/dashboard/account/tokens)")
    parser.add_argument("--password", help="Supabase database password (set during project creation)")
    parser.add_argument("--auto-migrate", action="store_true", help="Run full migration and delete local database upon success")
    args = parser.parse_args()

    print("=" * 70)
    print("[AUTOMATED SUPABASE SQL EXECUTOR]")
    print("=" * 70)

    if not os.path.exists(SCHEMA_PATH):
        print(f"[!] Schema file not found: {SCHEMA_PATH}")
        sys.exit(1)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        sql_content = f.read()

    token = args.token or os.getenv("SUPABASE_ACCESS_TOKEN", "").strip()
    password = args.password or os.getenv("SUPABASE_DB_PASSWORD", "").strip()

    if not token and not password:
        print("[!] No credentials provided.")
        print("    Please provide one of the following:")
        print("    Option 1: --token <SUPABASE_PERSONAL_ACCESS_TOKEN>")
        print("              Generate in 10s at: https://supabase.com/dashboard/account/tokens")
        print("    Option 2: --password <SUPABASE_DB_PASSWORD>")
        print("              The database password you set when creating the project")
        sys.exit(1)

    success = False
    if token:
        success = execute_via_management_api(token, sql_content)
    elif password:
        success = execute_via_postgres(password, sql_content)

    if success:
        print("\n[Step 2/2] Verifying table readiness...")
        if verify_table_ready():
            print("\n" + "=" * 70)
            print("[SUCCESS] Supabase database initialized and ready for cloud history!")
            print("=" * 70)
            
            if args.auto_migrate:
                print("\n[*] Starting automatic migration from local SQLite to Supabase...")
                from scripts.migrate_to_supabase import main as run_migration
                sys.argv = ["migrate_to_supabase.py", "--delete-local"]
                run_migration()
        else:
            print("[!] Table created but Data API schema cache may need a few seconds to refresh.")
    else:
        print("[!] Execution failed. Please check the credentials provided.")
        sys.exit(1)

if __name__ == "__main__":
    main()
