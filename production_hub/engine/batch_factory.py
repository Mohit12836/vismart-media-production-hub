#!/usr/bin/env python3
"""
Autonomous Multi-Channel Batch Factory & High-Concurrency Queue Engine
Capable of churning out 100+ Reels, Long Videos & Stories 24/7 on VPS
"""

import os
import sys
import json
import time
import uuid
import threading
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

# Ensure utf-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
QUEUE_FILE = BASE_DIR / "batch_queue.json"
MASTER_GENERATOR = BASE_DIR / "master_generator.py"

lock = threading.Lock()
worker_thread: Optional[threading.Thread] = None
should_stop = False

def load_queue_data() -> Dict:
    with lock:
        if not QUEUE_FILE.exists():
            init_data = {
                "is_running": False,
                "current_job_id": None,
                "jobs": []
            }
            with open(QUEUE_FILE, "w", encoding="utf-8") as f:
                json.dump(init_data, f, indent=2)
            return init_data
        try:
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"is_running": False, "current_job_id": None, "jobs": []}

def save_queue_data(data: Dict):
    with lock:
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

def add_batch_topics(
    topics: List[str],
    formats: List[str] = ["reel"],
    style: str = "silent_kinetic",
    mode: str = "silent",
    voice: str = "hi-IN-MadhurNeural",
    rate: str = "+12%",
    pitch: str = "+0Hz"
) -> int:
    """Adds a batch of topics and format variations to the queue."""
    data = load_queue_data()
    added_count = 0

    for topic in topics:
        topic_clean = topic.strip()
        if not topic_clean:
            continue
        for fmt in formats:
            # Map format to optimal style if not specified
            job_style = style
            if fmt == "long":
                job_style = "long_explainer"
            elif fmt == "story":
                job_style = "silent_kinetic"

            job = {
                "id": str(uuid.uuid4())[:8],
                "topic": topic_clean,
                "format": fmt,
                "style": job_style,
                "mode": mode,
                "voice": voice,
                "rate": rate,
                "pitch": pitch,
                "status": "pending",
                "output_file": None,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "finished_at": None,
                "error": None
            }
            data["jobs"].append(job)
            added_count += 1

    save_queue_data(data)
    print(f"[BatchFactory] Added {added_count} jobs to the production queue.")
    return added_count

def execute_job(job: Dict) -> bool:
    """Executes a single rendering job through master_generator."""
    fmt = job.get("format", "reel")
    style = job.get("style", "silent_kinetic")
    mode = job.get("mode", "silent")
    voice = job.get("voice", "hi-IN-MadhurNeural")
    rate = job.get("rate", "+12%")
    pitch = job.get("pitch", "+0Hz")
    topic = job.get("topic", "")

    # Category directory
    if fmt == "long" or style == "long_explainer":
        sub_dir = OUTPUTS_DIR / "long"
        prefix = "long"
    elif fmt == "story":
        sub_dir = OUTPUTS_DIR / "stories"
        prefix = "story"
    else:
        sub_dir = OUTPUTS_DIR / "reels"
        prefix = "reel"
    sub_dir.mkdir(parents=True, exist_ok=True)

    timestamp = int(time.time())
    out_file = sub_dir / f"{prefix}_{timestamp}_{job['id']}.mp4"

    cmd = [
        sys.executable,
        str(MASTER_GENERATOR),
        "--style", style,
        "--mode", mode,
        "--format", fmt,
        "--voice", voice,
        "--rate", rate,
        "--pitch", pitch,
        "--output", str(out_file)
    ]

    if mode == "voice" and topic:
        cmd.extend(["--text", topic])

    print(f"[BatchFactory Worker] Starting Job #{job['id']}: {topic[:40]} ({fmt.upper()})...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")

    if out_file.exists() and out_file.stat().st_size > 10000:
        job["status"] = "completed"
        job["output_file"] = str(out_file.relative_to(BASE_DIR)).replace("\\", "/")
        job["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[BatchFactory Worker] ✅ Job #{job['id']} COMPLETED: {out_file.name}")
        return True
    else:
        job["status"] = "failed"
        job["error"] = result.stderr or result.stdout or "Output file missing or empty"
        job["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[BatchFactory Worker] ❌ Job #{job['id']} FAILED: {job['error'][:100]}")
        return False

def _worker_loop():
    global should_stop
    print("[BatchFactory] Worker loop activated.")
    while not should_stop:
        data = load_queue_data()
        if not data.get("is_running", False):
            break

        # Find first pending job
        pending_job = None
        for j in data["jobs"]:
            if j["status"] == "pending":
                pending_job = j
                break

        if not pending_job:
            print("[BatchFactory] All queued jobs processed. Worker resting.")
            data["is_running"] = False
            data["current_job_id"] = None
            save_queue_data(data)
            break

        pending_job["status"] = "processing"
        data["current_job_id"] = pending_job["id"]
        save_queue_data(data)

        # Execute
        execute_job(pending_job)

        # Update and save
        for j in data["jobs"]:
            if j["id"] == pending_job["id"]:
                j.update(pending_job)
                break
        data["current_job_id"] = None
        save_queue_data(data)

        # Short rest to let CPU breathe
        time.sleep(2)

def start_worker() -> bool:
    global worker_thread, should_stop
    should_stop = False
    data = load_queue_data()
    data["is_running"] = True
    save_queue_data(data)

    if worker_thread is None or not worker_thread.is_alive():
        worker_thread = threading.Thread(target=_worker_loop, daemon=True)
        worker_thread.start()
        print("[BatchFactory] Worker thread successfully started.")
        return True
    return False

def pause_worker() -> bool:
    global should_stop
    should_stop = True
    data = load_queue_data()
    data["is_running"] = False
    save_queue_data(data)
    print("[BatchFactory] Worker signaled to pause.")
    return True

def clear_jobs(completed_only: bool = False):
    data = load_queue_data()
    if completed_only:
        data["jobs"] = [j for j in data["jobs"] if j["status"] != "completed"]
    else:
        data["jobs"] = []
        data["is_running"] = False
        data["current_job_id"] = None
    save_queue_data(data)

def get_queue_stats() -> Dict:
    data = load_queue_data()
    jobs = data.get("jobs", [])
    total = len(jobs)
    completed = sum(1 for j in jobs if j.get("status") == "completed")
    failed = sum(1 for j in jobs if j.get("status") == "failed")
    pending = sum(1 for j in jobs if j.get("status") == "pending")
    processing = sum(1 for j in jobs if j.get("status") == "processing")
    percent = round((completed / total * 100), 1) if total > 0 else 0

    reels_count = sum(1 for j in jobs if j.get("status") == "completed" and j.get("format") == "reel")
    long_count = sum(1 for j in jobs if j.get("status") == "completed" and j.get("format") == "long")
    stories_count = sum(1 for j in jobs if j.get("status") == "completed" and j.get("format") == "story")

    curr_job = next((j for j in jobs if j.get("id") == data.get("current_job_id")), None)

    return {
        "is_running": data.get("is_running", False),
        "total": total,
        "completed": completed,
        "failed": failed,
        "pending": pending,
        "processing": processing,
        "percent": percent,
        "counts": {
            "reels": reels_count,
            "long": long_count,
            "stories": stories_count
        },
        "current_job": curr_job,
        "jobs": jobs[-20:] # Return last 20 jobs for preview
    }
