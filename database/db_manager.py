"""
Database Manager for Accessibility Dashboard History.
Supports:
1. Supabase (via PostgreSQL URI or Supabase Python Client REST API)
2. Cloud PostgreSQL (Neon, Render, AWS RDS)
3. Local SQLite with automatic failover and migration utilities
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, select, delete, or_, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Automatically load environment variables
load_dotenv()

# Local SQLite fallback path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "database", "history.db")
SQLITE_URI = f"sqlite:///{DB_PATH}"

Base = declarative_base()

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String(50), nullable=False)
    doc_name = Column(String(255), nullable=False)
    file_type = Column(String(100), nullable=False)
    input_text = Column(Text, nullable=False)
    accessibility_score = Column(Float, nullable=False)
    readability_score = Column(Float, nullable=False)
    grade_level = Column(Float, nullable=False)
    reading_time = Column(Float, nullable=False)
    violations_count = Column(Integer, nullable=False)
    issues_json = Column(Text, nullable=False)
    metrics_json = Column(Text, nullable=False)
    simplified_text = Column(Text, nullable=True, default="")

    def to_dict(self) -> Dict[str, Any]:
        """Convert ORM model to dictionary."""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "doc_name": self.doc_name,
            "file_type": self.file_type,
            "input_text": self.input_text,
            "accessibility_score": self.accessibility_score,
            "readability_score": self.readability_score,
            "grade_level": self.grade_level,
            "reading_time": self.reading_time,
            "violations_count": self.violations_count,
            "issues_json": self.issues_json,
            "metrics_json": self.metrics_json,
            "simplified_text": self.simplified_text or "",
            "issues": json.loads(self.issues_json) if self.issues_json else [],
            "metrics": json.loads(self.metrics_json) if self.metrics_json else {}
        }

def normalize_database_url(url: Optional[str]) -> str:
    """Normalize PostgreSQL URL protocol and clean whitespaces."""
    if not url:
        return ""
    url = url.strip()
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://") and "+psycopg" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url

def get_configured_url() -> str:
    """Retrieve database URL from environment or fallback to SQLite."""
    raw_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or ""
    # Only use if not an unfilled template placeholder
    if raw_url and "[YOUR-" not in raw_url and "<password>" not in raw_url:
        env_url = normalize_database_url(raw_url)
        if env_url:
            return env_url
    return SQLITE_URI

def normalize_supabase_url(url: Optional[str]) -> str:
    """Normalize Supabase URL, stripping trailing /rest/v1 or slashes."""
    if not url:
        return ""
    url = url.strip().rstrip("/")
    if url.endswith("/rest/v1"):
        url = url[:-8]
    return url.rstrip("/")

def get_supabase_client():
    """Retrieve Supabase Python client if credentials configured."""
    raw_url = os.getenv("SUPABASE_URL", "").strip()
    url = normalize_supabase_url(raw_url)
    key = os.getenv("SUPABASE_KEY", "").strip() or os.getenv("SUPABASE_ANON_KEY", "").strip()
    if url and key:
        try:
            from supabase import create_client
            return create_client(url, key)
        except Exception:
            return None
    return None

def test_supabase_api(url: str, key: str) -> Tuple[bool, str]:
    """Test connecting to Supabase using REST API."""
    if not url or not key:
        return False, "Both Supabase Project URL and API Key are required."
    try:
        clean_url = normalize_supabase_url(url)
        from supabase import create_client
        client = create_client(clean_url, key.strip())
        try:
            res = client.table("analyses").select("id").limit(1).execute()
            return True, f"Connected to Supabase Data API! Table 'analyses' detected ({len(res.data)} sample rows)."
        except Exception as te:
            err_msg = str(te)
            if "relation \"public.analyses\" does not exist" in err_msg or "PGRST205" in err_msg or "schema cache" in err_msg:
                return True, "Connected to Supabase Data API! (Next step: run the table setup SQL in your Supabase SQL Editor)."
            return False, f"Supabase API error: {err_msg}"
    except Exception as e:
        return False, f"Supabase connection error: {str(e)}"

def get_engine(custom_url: Optional[str] = None):
    """Create SQLAlchemy engine with connection verification and safe fallback."""
    target_url = normalize_database_url(custom_url) if custom_url else get_configured_url()
    
    # If targeting PostgreSQL / Supabase
    if target_url.startswith("postgresql://"):
        try:
            engine = create_engine(target_url, pool_pre_ping=True, pool_recycle=300)
            # Quick connectivity check
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            db_type = "Supabase PostgreSQL" if "supabase" in target_url.lower() else "PostgreSQL"
            return engine, True, db_type
        except Exception as e:
            # Fall back to SQLite if PostgreSQL fails
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            fallback_engine = create_engine(SQLITE_URI)
            return fallback_engine, False, f"PostgreSQL connection failed ({e}), using SQLite fallback"
    
    # Local SQLite
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    engine = create_engine(SQLITE_URI)
    return engine, True, "SQLite"

def init_db(custom_url: Optional[str] = None) -> None:
    """Initialize database schema on target database."""
    if custom_url is None and get_supabase_client() is not None:
        # Supabase cloud is primary persistence layer, skip local SQLite creation
        return
    engine, _, _ = get_engine(custom_url)
    Base.metadata.create_all(engine)

def test_db_connection(url: str) -> Tuple[bool, str]:
    """Test connecting to a given database URI."""
    clean_url = normalize_database_url(url)
    if not clean_url:
        return False, "Database URL cannot be empty."
    try:
        engine = create_engine(clean_url, pool_pre_ping=True)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();" if "postgresql" in clean_url else "SELECT 1;"))
            ver = result.scalar()
        is_supabase = "supabase" in clean_url.lower()
        provider = "Supabase PostgreSQL" if is_supabase else "PostgreSQL"
        return True, f"Connected to {provider} successfully! {str(ver)[:60]}"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

def get_active_db_status() -> Dict[str, Any]:
    """Inspect and return current database connection metadata."""
    # 1. Check direct PostgreSQL / Supabase URI
    configured = get_configured_url()
    is_pg = configured.startswith("postgresql://")
    is_supabase_uri = is_pg and "supabase" in configured.lower()
    
    if is_pg:
        # Mask credentials
        try:
            parts = configured.split("@")
            masked_url = f"postgresql://***:***@{parts[1]}" if len(parts) > 1 else "postgresql://***"
        except Exception:
            masked_url = "postgresql://[configured]"
            
        success, msg = test_db_connection(configured)
        provider = "Supabase PostgreSQL" if is_supabase_uri else "PostgreSQL"
        return {
            "type": provider,
            "is_postgres": True,
            "is_supabase": is_supabase_uri,
            "connected": success,
            "display_url": masked_url,
            "message": msg if success else f"Offline: {msg}"
        }
        
    # 2. Check Supabase REST API credentials
    sb_url = os.getenv("SUPABASE_URL", "").strip()
    sb_key = os.getenv("SUPABASE_KEY", "").strip() or os.getenv("SUPABASE_ANON_KEY", "").strip()
    if sb_url and sb_key:
        ok, msg = test_supabase_api(sb_url, sb_key)
        return {
            "type": "Supabase REST",
            "is_postgres": False,
            "is_supabase": True,
            "connected": ok,
            "display_url": sb_url,
            "message": msg
        }
        
    # 3. Default SQLite
    return {
        "type": "SQLite",
        "is_postgres": False,
        "is_supabase": False,
        "connected": True,
        "display_url": f"Local File: {os.path.basename(DB_PATH)}",
        "message": "Local persistent SQLite active"
    }

def save_analysis(
    doc_name: str,
    file_type: str,
    input_text: str,
    accessibility_score: float,
    readability_score: float,
    grade_level: float,
    reading_time: float,
    violations_count: int,
    issues: List[Dict[str, Any]],
    metrics: Dict[str, Any],
    simplified_text: str = "",
    custom_url: Optional[str] = None
) -> int:
    """Save an analysis record into active database."""
    # Try Supabase REST if configured and no custom DB url
    sb_client = get_supabase_client()
    configured_url = custom_url or get_configured_url()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    issues_json = json.dumps(issues)
    metrics_json = json.dumps(metrics)
    
    # If Supabase client configured and not using custom PostgreSQL URL
    if sb_client and configured_url.startswith("sqlite://"):
        try:
            record_data = {
                "timestamp": timestamp,
                "doc_name": doc_name,
                "file_type": file_type,
                "input_text": input_text,
                "accessibility_score": accessibility_score,
                "readability_score": readability_score,
                "grade_level": grade_level,
                "reading_time": reading_time,
                "violations_count": violations_count,
                "issues_json": issues_json,
                "metrics_json": metrics_json,
                "simplified_text": simplified_text
            }
            res = sb_client.table("analyses").insert(record_data).execute()
            if res.data and len(res.data) > 0:
                return res.data[0].get("id", 1)
        except Exception as e:
            print(f"Supabase REST insert failed, falling back to local SQLite: {e}")
            
    # Standard SQLAlchemy ORM (Supabase PostgreSQL / Cloud PostgreSQL / SQLite)
    init_db(custom_url)
    engine, _, _ = get_engine(custom_url)
    Session = sessionmaker(bind=engine)
    
    record = Analysis(
        timestamp=timestamp,
        doc_name=doc_name,
        file_type=file_type,
        input_text=input_text,
        accessibility_score=accessibility_score,
        readability_score=readability_score,
        grade_level=grade_level,
        reading_time=reading_time,
        violations_count=violations_count,
        issues_json=issues_json,
        metrics_json=metrics_json,
        simplified_text=simplified_text
    )
    
    with Session() as session:
        session.add(record)
        session.commit()
        session.refresh(record)
        analysis_id = record.id
        
    return analysis_id

def get_history(search_query: str = "", limit: int = 50, custom_url: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve history of saved analyses with optional search filtering."""
    sb_client = get_supabase_client()
    configured_url = custom_url or get_configured_url()
    
    if sb_client and configured_url.startswith("sqlite://"):
        try:
            query = sb_client.table("analyses").select("*").order("id", desc=True).limit(limit)
            if search_query:
                pattern = f"%{search_query.lower()}%"
                query = query.or_(f"doc_name.ilike.{pattern},input_text.ilike.{pattern}")
            res = query.execute()
            data = res.data or []
            for item in data:
                item["issues"] = json.loads(item["issues_json"]) if item.get("issues_json") else []
                item["metrics"] = json.loads(item["metrics_json"]) if item.get("metrics_json") else {}
            return data
        except Exception as e:
            print(f"Supabase REST query failed, falling back to SQLite: {e}")

    init_db(custom_url)
    engine, _, _ = get_engine(custom_url)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        stmt = select(Analysis).order_by(Analysis.id.desc()).limit(limit)
        if search_query:
            pattern = f"%{search_query.lower()}%"
            stmt = stmt.where(
                or_(
                    Analysis.doc_name.ilike(pattern),
                    Analysis.input_text.ilike(pattern)
                )
            )
        records = session.execute(stmt).scalars().all()
        return [rec.to_dict() for rec in records]

def get_analysis_by_id(analysis_id: int, custom_url: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Get a single analysis by ID."""
    sb_client = get_supabase_client()
    configured_url = custom_url or get_configured_url()
    
    if sb_client and configured_url.startswith("sqlite://"):
        try:
            res = sb_client.table("analyses").select("*").eq("id", analysis_id).limit(1).execute()
            if res.data:
                item = res.data[0]
                item["issues"] = json.loads(item["issues_json"]) if item.get("issues_json") else []
                item["metrics"] = json.loads(item["metrics_json"]) if item.get("metrics_json") else {}
                return item
        except Exception:
            pass

    init_db(custom_url)
    engine, _, _ = get_engine(custom_url)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        record = session.get(Analysis, analysis_id)
        if record:
            return record.to_dict()
    return None

def delete_analysis(analysis_id: int, custom_url: Optional[str] = None) -> bool:
    """Delete an analysis record by ID."""
    sb_client = get_supabase_client()
    configured_url = custom_url or get_configured_url()
    
    if sb_client and configured_url.startswith("sqlite://"):
        try:
            res = sb_client.table("analyses").delete().eq("id", analysis_id).execute()
            return True
        except Exception:
            pass

    init_db(custom_url)
    engine, _, _ = get_engine(custom_url)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        record = session.get(Analysis, analysis_id)
        if record:
            session.delete(record)
            session.commit()
            return True
    return False

def clear_all_history(custom_url: Optional[str] = None) -> bool:
    """Clear all analysis records from history database."""
    sb_client = get_supabase_client()
    configured_url = custom_url or get_configured_url()
    
    if sb_client and configured_url.startswith("sqlite://"):
        try:
            # Delete records where id > 0
            sb_client.table("analyses").delete().gt("id", 0).execute()
            return True
        except Exception:
            pass

    init_db(custom_url)
    engine, _, _ = get_engine(custom_url)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        session.execute(delete(Analysis))
        session.commit()
    return True

def migrate_sqlite_to_postgres(postgres_url: str) -> Tuple[bool, int, str]:
    """Copy all records from local SQLite into remote Supabase/PostgreSQL database."""
    clean_pg_url = normalize_database_url(postgres_url)
    ok, msg = test_db_connection(clean_pg_url)
    if not ok:
        return False, 0, f"Cannot connect to database: {msg}"
        
    try:
        # 1. Fetch from SQLite
        sqlite_records = get_history(custom_url=SQLITE_URI, limit=10000)
        if not sqlite_records:
            return True, 0, "No records found in local SQLite database to migrate."
            
        # 2. Init target table
        init_db(custom_url=clean_pg_url)
        pg_engine = create_engine(clean_pg_url)
        PgSession = sessionmaker(bind=pg_engine)
        
        migrated_count = 0
        with PgSession() as pg_session:
            for rec in sqlite_records:
                pg_record = Analysis(
                    timestamp=rec["timestamp"],
                    doc_name=rec["doc_name"],
                    file_type=rec["file_type"],
                    input_text=rec["input_text"],
                    accessibility_score=rec["accessibility_score"],
                    readability_score=rec["readability_score"],
                    grade_level=rec["grade_level"],
                    reading_time=rec["reading_time"],
                    violations_count=rec["violations_count"],
                    issues_json=rec["issues_json"],
                    metrics_json=rec["metrics_json"],
                    simplified_text=rec.get("simplified_text", "")
                )
                pg_session.add(pg_record)
                migrated_count += 1
            pg_session.commit()
            
        is_sb = "supabase" in clean_pg_url.lower()
        target_name = "Supabase" if is_sb else "PostgreSQL"
        return True, migrated_count, f"Successfully migrated {migrated_count} records to {target_name}!"
    except Exception as e:
        return False, 0, f"Migration failed: {str(e)}"

def save_supabase_credentials(
    db_url: Optional[str] = None,
    supabase_url: Optional[str] = None,
    supabase_key: Optional[str] = None
) -> bool:
    """Save Supabase credentials to .env file."""
    env_path = os.path.join(PROJECT_ROOT, ".env")
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
    updates = {}
    if db_url is not None:
        updates["DATABASE_URL"] = normalize_database_url(db_url)
    if supabase_url is not None:
        updates["SUPABASE_URL"] = supabase_url.strip()
    if supabase_key is not None:
        updates["SUPABASE_KEY"] = supabase_key.strip()
        
    new_lines = []
    processed_keys = set()
    for line in lines:
        matched = False
        for k, v in updates.items():
            if line.strip().startswith(f"{k}="):
                new_lines.append(f"{k}={v}\n")
                processed_keys.add(k)
                matched = True
                break
        if not matched:
            new_lines.append(line)
            
    for k, v in updates.items():
        if k not in processed_keys:
            new_lines.append(f"{k}={v}\n")
            
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
        
    for k, v in updates.items():
        os.environ[k] = v
        
    return True

def save_db_url_to_env(db_url: str) -> bool:
    """Backward compatible helper to save DATABASE_URL."""
    return save_supabase_credentials(db_url=db_url)

def is_local_db_present() -> bool:
    """Check if local SQLite database file exists."""
    return os.path.exists(DB_PATH)

def delete_local_db() -> Tuple[bool, str]:
    """Archive and delete local SQLite database."""
    if not os.path.exists(DB_PATH):
        return True, "Local database is already deleted. Running in Cloud-Only mode."
    try:
        backup_dir = os.path.join(PROJECT_ROOT, "database", "backups")
        os.makedirs(backup_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"history_backup_{ts}.db")
        import shutil
        shutil.copy2(DB_PATH, backup_path)
        os.remove(DB_PATH)
        return True, f"Local database archived to '{os.path.basename(backup_path)}' and deleted! Dashboard is now 100% Cloud-Only."
    except Exception as e:
        return False, f"Error deleting local database: {str(e)}"

def migrate_local_sqlite_to_supabase() -> Tuple[bool, int, str]:
    """Transfer records directly from local SQLite to Supabase via client."""
    sb_client = get_supabase_client()
    if not sb_client:
        return False, 0, "Supabase client not configured. Set SUPABASE_URL and SUPABASE_KEY first."
        
    ok, msg = test_supabase_api(os.getenv("SUPABASE_URL", ""), os.getenv("SUPABASE_KEY", ""))
    if not ok:
        return False, 0, f"Cannot connect to Supabase: {msg}"
        
    if not os.path.exists(DB_PATH):
        return True, 0, "No local SQLite database found to migrate."
        
    try:
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analyses ORDER BY id ASC")
        rows = cursor.fetchall()
        records = [dict(r) for r in rows]
        conn.close()
        
        if not records:
            return True, 0, "Local SQLite database has 0 records."
            
        payload_batch = []
        for r in records:
            payload_batch.append({
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
            })
            
        res = sb_client.table("analyses").insert(payload_batch).execute()
        count = len(res.data) if res.data else len(payload_batch)
        return True, count, f"Successfully transferred {count} record(s) to Supabase!"
    except Exception as e:
        return False, 0, f"Migration failed: {str(e)}"

