import os
import sys
import json
import asyncio
import glob
import subprocess
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, BackgroundTasks, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import Batch Factory Engine
sys.path.append(str(Path(__file__).resolve().parent.parent))
from engine.batch_factory import (
    add_batch_topics,
    start_worker as start_batch_worker,
    pause_worker as pause_batch_worker,
    clear_jobs as clear_batch_jobs,
    get_queue_stats
)

# Ensure utf-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR = Path(__file__).resolve().parent / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Path to python master_generator
MASTER_GENERATOR = BASE_DIR / "master_generator.py"
VOICE_ENGINE = BASE_DIR / "engine" / "voice_engine.py"

app = FastAPI(title="Vismart Autonomous Media Production Hub")

# State tracking for ongoing render
render_state = {
    "is_rendering": False,
    "last_status": "Ready",
    "last_video": None,
    "last_error": None,
    "scheduler_active": False,
    "schedule_time": "10:00",
    "schedule_style": "silent_kinetic",
    "schedule_mode": "silent"
}

class RenderRequest(BaseModel):
    mode: str = "voice"            # "voice" or "silent"
    style: str = "silent_kinetic"   # "silent_kinetic", "vismart", "agency_ui"
    text: Optional[str] = None
    voice: str = "hi-IN-MadhurNeural"
    rate: str = "+10%"
    pitch: str = "+0Hz"
    custom_output_name: Optional[str] = None

class ScheduleSlot(BaseModel):
    id: str
    label: str
    active: bool
    time_str: str
    style: str
    mode: str
    prompt: Optional[str] = ""

class MultiScheduleRequest(BaseModel):
    slots: list[ScheduleSlot]

def run_render_task(req_dict: dict):
    global render_state
    render_state["is_rendering"] = True
    render_state["last_status"] = "Rendering in progress..."
    render_state["last_error"] = None

    out_name = req_dict.get("custom_output_name")
    if not out_name:
        import time
        out_name = f"reel_{int(time.time())}.mp4"
    if not out_name.endswith(".mp4"):
        out_name += ".mp4"

    out_path = OUTPUTS_DIR / out_name

    cmd = [
        sys.executable,
        str(MASTER_GENERATOR),
        "--style", req_dict.get("style", "silent_kinetic"),
        "--mode", req_dict.get("mode", "voice"),
        "--output", str(out_path)
    ]

    if req_dict.get("mode") == "voice":
        cmd.extend([
            "--voice", req_dict.get("voice", "hi-IN-MadhurNeural"),
            "--rate", req_dict.get("rate", "+10%"),
            "--pitch", req_dict.get("pitch", "+0Hz")
        ])
        if req_dict.get("text"):
            cmd.extend(["--text", req_dict.get("text")])

    print(f"[DashboardAPI] Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")

    render_state["is_rendering"] = False
    if out_path.exists() and out_path.stat().st_size > 10000:
        render_state["last_status"] = "Completed Successfully"
        render_state["last_video"] = out_name
        print(f"[DashboardAPI] Render SUCCESS: {out_name}")
    else:
        render_state["last_status"] = "Render Failed"
        render_state["last_error"] = result.stderr or result.stdout
        print(f"[DashboardAPI] Render FAILED: {result.stderr}")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return HTMLResponse("<h1>Dashboard Loading...</h1>")
    with open(index_file, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/api/status")
async def get_status():
    return JSONResponse(render_state)

@app.post("/api/render")
async def trigger_render(req: RenderRequest, bg_tasks: BackgroundTasks):
    global render_state
    if render_state["is_rendering"]:
        raise HTTPException(status_code=400, detail="A video is already rendering. Please wait.")
    bg_tasks.add_task(run_render_task, req.model_dump())
    return JSONResponse({"status": "queued", "message": "Video rendering started in background"})

class BatchSubmitRequest(BaseModel):
    topics: list[str]
    formats: list[str] = ["reel"]
    style: str = "silent_kinetic"
    mode: str = "silent"
    voice: str = "hi-IN-MadhurNeural"
    rate: str = "+12%"
    pitch: str = "+0Hz"
    auto_start: bool = True

@app.post("/api/batch/submit")
async def submit_batch(req: BatchSubmitRequest):
    count = add_batch_topics(
        topics=req.topics,
        formats=req.formats,
        style=req.style,
        mode=req.mode,
        voice=req.voice,
        rate=req.rate,
        pitch=req.pitch
    )
    if req.auto_start:
        start_batch_worker()
    return JSONResponse({"status": "queued", "added_jobs": count})

@app.get("/api/batch/status")
async def batch_status():
    return JSONResponse(get_queue_stats())

@app.post("/api/batch/start")
async def batch_start():
    started = start_batch_worker()
    return JSONResponse({"status": "started" if started else "already_running"})

@app.post("/api/batch/pause")
async def batch_pause():
    pause_batch_worker()
    return JSONResponse({"status": "paused"})

@app.post("/api/batch/clear")
async def batch_clear(completed_only: bool = False):
    clear_batch_jobs(completed_only=completed_only)
    return JSONResponse({"status": "cleared"})

@app.get("/api/videos")
async def list_videos():
    videos = []
    # Search all mp4s recursively in outputs/
    for mp4 in sorted(glob.glob(str(OUTPUTS_DIR / "**/*.mp4"), recursive=True), key=os.path.getmtime, reverse=True):
        fname = os.path.basename(mp4)
        rel_path = os.path.relpath(mp4, str(OUTPUTS_DIR)).replace("\\", "/")
        cover_path = mp4.replace(".mp4", "_cover.png")
        has_cover = os.path.exists(cover_path)
        cover_rel = rel_path.replace(".mp4", "_cover.png")
        
        # Categorize
        if "/long/" in rel_path or "long_" in fname:
            cat = "long"
        elif "/stories/" in rel_path or "story_" in fname:
            cat = "story"
        else:
            cat = "reel"

        size_mb = round(os.path.getsize(mp4) / (1024 * 1024), 2)
        mtime = os.path.getmtime(mp4)
        videos.append({
            "filename": fname,
            "url": f"/outputs/{rel_path}",
            "cover_url": f"/outputs/{cover_rel}" if has_cover else None,
            "category": cat,
            "size_mb": size_mb,
            "mtime": mtime
        })
    return JSONResponse({"videos": videos})

@app.get("/api/preview-voice")
async def preview_voice(text: str = Query(..., min_length=2), voice: str = "hi-IN-MadhurNeural", rate: str = "+10%", pitch: str = "+0Hz"):
    """Generates a 3-second live audio preview with rate and pitch controls"""
    preview_file = STATIC_DIR / "temp_preview.mp3"
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await communicate.save(str(preview_file))
        return FileResponse(str(preview_file), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

SCHEDULES_FILE = BASE_DIR / "schedules.json"

DEFAULT_SCHEDULES = [
    {
        "id": "morning",
        "label": "🌅 Slot 1: Morning Viral Reel",
        "active": True,
        "time_str": "10:00",
        "style": "silent_kinetic",
        "mode": "silent",
        "prompt": "Top 3 Dental Clinic Marketing Hacks in 2026"
    },
    {
        "id": "evening",
        "label": "🌆 Slot 2: Evening Explainer Story",
        "active": True,
        "time_str": "18:00",
        "style": "vismart",
        "mode": "voice",
        "prompt": "Why modern clinics lose ₹2 Lakhs without an Apple-grade booking website"
    }
]

@app.get("/api/schedules")
async def get_schedules():
    if not SCHEDULES_FILE.exists():
        with open(SCHEDULES_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_SCHEDULES, f, indent=2)
    with open(SCHEDULES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return JSONResponse({"slots": data})

@app.post("/api/schedules")
async def save_schedules(req: MultiScheduleRequest):
    data = [s.model_dump() for s in req.slots]
    with open(SCHEDULES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return JSONResponse({"status": "saved", "slots": data})

@app.get("/api/vps-tools")
async def check_vps_tools():
    """Checks the status of tools running on VPS: Hermes (9119), n8n (5678), MoneyPrinter (8501)"""
    return JSONResponse({
        "vps_ip": "72.61.232.114",
        "hermes_agent": {"port": 9119, "url": "http://72.61.232.114:9119", "role": "Autonomous Brain & Script Writer"},
        "money_printer": {"port": 8501, "url": "http://72.61.232.114:8501", "role": "AI Shorts Generator"},
        "n8n_automation": {"port": 5678, "url": "http://72.61.232.114:5678", "role": "Cron & Cloud Drive Scheduler"},
        "langflow": {"port": 7860, "url": "http://72.61.232.114:7860", "role": "Visual Agent Pipeline"}
    })

# Serve generated videos and covers directly
app.mount("/outputs", StaticFiles(directory=str(OUTPUTS_DIR)), name="outputs")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=False)
