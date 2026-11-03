"""Transactional, restart-safe queue. A single rendering process owns the worker."""
import hashlib
import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from pathlib import Path
from .recipes import RECIPES

BASE = Path(__file__).resolve().parents[1]
DB = Path(os.environ.get("FACTORY_DB", BASE / "runtime" / "factory.db"))

def now():
    return datetime.now(timezone.utc).isoformat()

@contextmanager
def connection():
    DB.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB, timeout=30)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init():
    with connection() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS channels(id TEXT PRIMARY KEY, name TEXT NOT NULL, config TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS automations(id TEXT PRIMARY KEY, channel_id TEXT NOT NULL REFERENCES channels(id), name TEXT NOT NULL, config TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS jobs(
          id TEXT PRIMARY KEY, automation_id TEXT NOT NULL REFERENCES automations(id), channel_id TEXT NOT NULL REFERENCES channels(id),
          fingerprint TEXT NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0, output TEXT, error TEXT,
          qa TEXT, approved_hash TEXT, drive_id TEXT, publish_id TEXT, delivery_attempted INTEGER NOT NULL DEFAULT 0,
          UNIQUE(channel_id, fingerprint));
        CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, job_id TEXT, action TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT NOT NULL);
        INSERT OR IGNORE INTO settings VALUES('enabled','1');
        ''')

def unpack(row):
    data = dict(row)
    for key in ("config", "payload", "qa"):
        if data.get(key):
            data[key] = json.loads(data[key])
    return data

def list_rows(table):
    if table not in ("channels", "automations", "jobs"):
        raise ValueError("Unknown collection")
    with connection() as db:
        return [unpack(r) for r in db.execute(f"SELECT * FROM {table} ORDER BY rowid DESC LIMIT 500")]

def get_job(job_id):
    with connection() as db:
        row = db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        if not row:
            raise ValueError("Job not found")
        return unpack(row)

def channel(data, item_id=None):
    name = str(data.get("name", "")).strip()
    if not name or len(name) > 100:
        raise ValueError("Channel name required (max 100 characters)")
    editing = item_id is not None
    item_id = item_id or uuid.uuid4().hex
    config = {"language": str(data.get("language", "hi"))[:30], "brand": name,
              "accent": data.get("accent", "#2563eb"), "destination": str(data.get("destination", ""))[:200] or item_id}
    import re
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", config["accent"]):
        raise ValueError("Accent must be a hex colour")
    with connection() as db:
        if editing:
            cursor = db.execute("UPDATE channels SET name=?,config=? WHERE id=?", (name, json.dumps(config), item_id))
            if not cursor.rowcount:
                raise ValueError("Channel not found")
        else:
            db.execute("INSERT INTO channels VALUES(?,?,?)", (item_id, name, json.dumps(config)))
    return item_id

def automation(data, item_id=None):
    recipe = data.get("recipe")
    fmt = data.get("format", "reel")
    if recipe not in RECIPES or fmt not in RECIPES[recipe]["formats"]:
        raise ValueError("Choose a supported recipe and format")
    name = str(data.get("name", "")).strip()
    limit = int(data.get("daily_limit", 10))
    if not name or len(name) > 100 or not 1 <= limit <= 100:
        raise ValueError("Name required; daily limit must be 1–100")
    mode = data.get("mode", "silent")
    if mode not in ("silent", "voice"):
        raise ValueError("Mode must be silent or voice")
    config = {"recipe": recipe, "format": fmt, "daily_limit": limit, "mode": mode,
              "voice": str(data.get("voice", "hi-IN-MadhurNeural"))[:100]}
    editing = item_id is not None
    item_id = item_id or uuid.uuid4().hex
    with connection() as db:
        if not db.execute("SELECT 1 FROM channels WHERE id=?", (data.get("channel_id"),)).fetchone():
            raise ValueError("Channel not found")
        if editing:
            cursor = db.execute("UPDATE automations SET channel_id=?,name=?,config=? WHERE id=?", (data["channel_id"], name, json.dumps(config), item_id))
            if not cursor.rowcount:
                raise ValueError("Automation not found")
        else:
            db.execute("INSERT INTO automations VALUES(?,?,?,?)", (item_id, data["channel_id"], name, json.dumps(config)))
    return item_id

def submit(automation_id, items):
    if not 1 <= len(items) <= 100:
        raise ValueError("Submit 1–100 scripts per request")
    with connection() as db:
        db.execute("BEGIN IMMEDIATE")
        auto = db.execute("SELECT * FROM automations WHERE id=?", (automation_id,)).fetchone()
        if not auto:
            raise ValueError("Automation not found")
        config = json.loads(auto["config"])
        channel_config = json.loads(db.execute("SELECT config FROM channels WHERE id=?", (auto["channel_id"],)).fetchone()[0])
        prepared = []
        for item in items:
            if item.get("rights_confirmed") is not True:
                raise ValueError("Confirm factual review and media rights before submitting")
            if not isinstance(item.get("scenes"), list):
                raise ValueError("Scenes must be an array")
            lines = [str(s).strip() for s in item.get("scenes", []) if str(s).strip()]
            if not 2 <= len(lines) <= 120 or any(len(s) > 240 for s in lines):
                raise ValueError("Each script needs 2–120 scenes, max 240 characters per scene")
            duration = int(item.get("duration", 25))
            low, high = (31, 900) if config["format"] == "long" else (10, 60)
            if not low <= duration <= high or duration / len(lines) < 2:
                raise ValueError(f"Duration must be {low}–{high}s with at least 2s per scene")
            assets = item.get("assets", [])
            if not isinstance(assets, list) or len(assets) > 120:
                raise ValueError("Assets must be a list of local image filenames")
            if assets and any(not isinstance(a, str) or Path(a).name != a or Path(a).suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp") for a in assets):
                raise ValueError("Use image filenames from hindi-reel/public/factory-assets")
            if config["recipe"] == "photo_story" and len(assets) != len(lines):
                raise ValueError("Photo stories need one image asset per scene")
            # Same copy on the same channel is a duplicate, even under another recipe.
            fingerprint = hashlib.sha256(" ".join(" ".join(lines).casefold().split()).encode()).hexdigest()
            payload = {**config, "scenes": lines, "duration": duration, "assets": assets,
                       "title": str(item.get("title", lines[0]))[:180], "brand": channel_config["brand"],
                       "accent": channel_config["accent"], "destination": channel_config["destination"],
                       "sources": str(item.get("sources", ""))[:4000], "rights_confirmed": item.get("rights_confirmed") is True}
            prepared.append((fingerprint, payload))
        added, duplicates = [], 0
        for fingerprint, payload in prepared:
            job_id = uuid.uuid4().hex
            status = "waiting_assets" if RECIPES[config["recipe"]]["kind"] == "external" else "pending"
            cursor = db.execute("INSERT OR IGNORE INTO jobs(id,automation_id,channel_id,fingerprint,status,payload,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)",
                                (job_id, automation_id, auto["channel_id"], fingerprint, status, json.dumps(payload, ensure_ascii=False), now(), now()))
            if cursor.rowcount:
                added.append(job_id)
            else:
                duplicates += 1
    return {"added": added, "duplicates": duplicates}

def update(job_id, **fields):
    allowed = {"status", "output", "error", "qa", "approved_hash", "drive_id", "publish_id", "delivery_attempted"}
    if not fields or not set(fields) <= allowed:
        raise ValueError("Invalid update")
    if isinstance(fields.get("qa"), dict):
        fields["qa"] = json.dumps(fields["qa"])
    fields["updated_at"] = now()
    with connection() as db:
        db.execute("UPDATE jobs SET " + ",".join(f"{key}=?" for key in fields) + " WHERE id=?", (*fields.values(), job_id))

def transition(job_id, old_status, new_status, **fields):
    if not set(fields) <= {"approved_hash", "error"}:
        raise ValueError("Invalid transition")
    with connection() as db:
        updates = ",".join(f"{key}=?" for key in fields)
        cursor = db.execute("UPDATE jobs SET status=?,updated_at=?" + ("," + updates if updates else "") + " WHERE id=? AND status=?", (new_status, now(), *fields.values(), job_id, old_status))
        if cursor.rowcount != 1:
            raise ValueError("Job state changed; refresh and try again")
        db.execute("INSERT INTO events(job_id,action,created_at) VALUES(?,?,?)", (job_id, new_status, now()))

def claim():
    day = datetime.now(timezone(timedelta(hours=5, minutes=30))).date().isoformat()
    with connection() as db:
        db.execute("BEGIN IMMEDIATE")
        if db.execute("SELECT value FROM settings WHERE key='enabled'").fetchone()[0] != '1':
            return None
        # Limit actual starts, including failures, per automation and globally per IST day.
        starts = db.execute("SELECT action FROM events WHERE action LIKE ?", (f"start:{day}:%",)).fetchall()
        if len(starts) >= int(os.environ.get("FACTORY_DAILY_LIMIT", "100")):
            return None
        counts = {}
        for r in starts:
            auto_id = r[0].split(":")[-1]
            counts[auto_id] = counts.get(auto_id, 0) + 1
        rows = db.execute("SELECT jobs.*, automations.config AS auto_config FROM jobs JOIN automations ON automations.id=jobs.automation_id WHERE status='pending' ORDER BY jobs.rowid").fetchall()
        for row in rows:
            if counts.get(row["automation_id"], 0) >= json.loads(row["auto_config"])["daily_limit"]:
                continue
            db.execute("UPDATE jobs SET status='rendering', attempts=attempts+1, updated_at=? WHERE id=?", (now(), row["id"]))
            db.execute("INSERT INTO events(job_id,action,created_at) VALUES(?,?,?)", (row["id"], f"start:{day}:{row['automation_id']}", now()))
            return unpack(row)
    return None

def enabled(value=None):
    with connection() as db:
        if value is not None:
            db.execute("UPDATE settings SET value=? WHERE key='enabled'", ('1' if value else '0',))
        return db.execute("SELECT value FROM settings WHERE key='enabled'").fetchone()[0] == '1'
