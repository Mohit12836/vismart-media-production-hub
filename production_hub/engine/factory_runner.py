"""One renderer per VPS, isolated props/audio, technical QA and approval-bound delivery."""
import asyncio
import hashlib
import json
import os
import shutil
import subprocess
import threading
from pathlib import Path
from . import factory_store as store
from .recipes import RECIPES

ROOT = store.BASE.parent
OUTPUTS = store.BASE / "outputs" / "factory"
REMOTION = ROOT / "hindi-reel"
worker = None
stop = threading.Event()
guard = threading.Lock()

def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def qa(path, payload):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture_output=True, text=True, timeout=60, check=True)
    info = json.loads(result.stdout)
    video = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    expected = (1920, 1080) if payload["format"] == "long" else (1080, 1920)
    if not video or (video["width"], video["height"]) != expected or video.get("codec_name") != "h264":
        raise ValueError(f"Expected H.264 video at {expected[0]}×{expected[1]}")
    seconds = float(info["format"]["duration"])
    if abs(seconds - payload["duration"]) > 1.1:
        raise ValueError("Video duration does not match the approved script plan")
    if payload["mode"] == "voice" and not any(s["codec_type"] == "audio" for s in info["streams"]):
        raise ValueError("Narrated video has no audio stream")
    return {"passed": True, "duration": seconds, "width": expected[0], "height": expected[1],
            "sha256": digest(path), "scope": "Technical checks only; facts, readability, pacing and rights need human review"}

def render(job):
    if shutil.disk_usage(store.BASE).free < 2 * 1024 ** 3:
        store.enabled(False)
        raise RuntimeError("Less than 2 GB free disk. New renders paused; free space before resuming.")
    payload = job["payload"]
    folder = OUTPUTS / job["channel_id"] / job["id"]
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "final.mp4"
    props = {"scenes": payload["scenes"], "duration": payload["duration"], "format": payload["format"],
             "layout": RECIPES[payload["recipe"]].get("layout", "story"), "brand": payload["brand"],
             "accent": payload["accent"], "assets": payload["assets"], "audio": None}
    if payload["mode"] == "voice":
        from .voice_engine import generate_speech
        audio_rel = f"factory-audio/{job['id']}.mp3"
        audio_path = REMOTION / "public" / audio_rel
        try:
            seconds = asyncio.run(generate_speech(" ".join(payload["scenes"]), str(audio_path), voice=payload["voice"], rate="+0%"))
            if seconds > payload["duration"] - 0.25:
                raise ValueError(f"Voice is {seconds}s; shorten copy or increase duration (no silent truncation)")
            props["audio"] = audio_rel
            shutil.copyfile(audio_path, folder / "voice.mp3")
        except Exception:
            audio_path.unlink(missing_ok=True)
            raise
    for asset in payload["assets"]:
        path = REMOTION / "public" / "factory-assets" / asset
        if not path.is_file():
            raise ValueError(f"Image asset missing: {asset}")
    props_file = folder / "props.json"
    props_file.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
    cli = REMOTION / "node_modules" / "@remotion" / "cli" / "remotion-cli.js"
    command = ["node", str(cli), "render", "src/factory-index.tsx", "FactoryVideo", str(target),
               f"--props={props_file}", "--codec=h264", "--crf=20", "--concurrency=1"]
    with open(folder / "render.log", "w", encoding="utf-8") as log:
        result = subprocess.run(command, cwd=REMOTION, stdout=log, stderr=subprocess.STDOUT, timeout=7200)
    if result.returncode or not target.is_file():
        raise RuntimeError("Render failed; inspect the job's render.log")
    return finish(job, target)

def finish(job, path):
    report = qa(path, job["payload"])
    folder = path.parent
    (folder / "script.txt").write_text("\n\n".join(job["payload"]["scenes"]), encoding="utf-8")
    (folder / "caption.txt").write_text(job["payload"]["title"], encoding="utf-8")
    (folder / "manifest.json").write_text(json.dumps({"id": job["id"], "channel_id": job["channel_id"], "payload": job["payload"], "qa": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    # A real frame from the final video is the cover.
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", str(path), "-frames:v", "1", str(folder / "cover.jpg")], capture_output=True, timeout=60, check=True)
    store.update(job["id"], status="awaiting_approval", output=str(path.relative_to(store.BASE)).replace("\\", "/"), qa=report, error=None)
    return report

def approve(job_id):
    job = store.get_job(job_id)
    if job["status"] != "awaiting_approval" or not job.get("qa", {}).get("passed"):
        raise ValueError("Only a technically checked video can be approved")
    if not job["payload"]["rights_confirmed"]:
        raise ValueError("Confirm sources and media rights when submitting the script")
    path = store.BASE / job["output"]
    current_hash = digest(path)
    if current_hash != job["qa"]["sha256"]:
        raise ValueError("File changed after quality check; re-render before approval")
    store.transition(job_id, "awaiting_approval", "approved", approved_hash=current_hash)

def integrations():
    return {
        "drive": {"configured": all(os.environ.get(k) for k in ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN", "GOOGLE_DRIVE_FOLDER_ID"))},
        "publisher": {"configured": bool(os.environ.get("FACTORY_PUBLISH_WEBHOOK") and os.environ.get("FACTORY_PUBLISH_SECRET"))},
        "canva": {"configured": False, "note": "Use Canva MCP in chat; VPS automation requires separate OAuth or an n8n workflow. Import its MP4 here."},
        "flow": {"configured": False, "note": "Import the edited MP4 from your Flow workflow; no provider credits spent by this engine."}}

def drive_upload(job):
    """Upload a deterministic folder of files. appProperties prevents duplicate Drive files on retry."""
    import requests
    keys = ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN", "GOOGLE_DRIVE_FOLDER_ID")
    if not all(os.environ.get(k) for k in keys):
        raise ValueError("Google Drive OAuth and destination folder are not configured")
    response = requests.post("https://oauth2.googleapis.com/token", data={"client_id": os.environ[keys[0]], "client_secret": os.environ[keys[1]], "refresh_token": os.environ[keys[2]], "grant_type": "refresh_token"}, timeout=30)
    response.raise_for_status()
    headers = {"Authorization": "Bearer " + response.json()["access_token"]}
    base = "https://www.googleapis.com/drive/v3/files"
    parent = os.environ[keys[3]]
    if not parent.isalnum() and not all(c.isalnum() or c in "_-" for c in parent):
        raise ValueError("Invalid Drive folder ID")
    folder = store.BASE / job["output"]
    final_id = None
    import mimetypes
    for path in [folder, folder.with_name("cover.jpg"), folder.with_name("caption.txt"), folder.with_name("script.txt"), folder.with_name("manifest.json")]:
        query = f"'{parent}' in parents and trashed = false and appProperties has {{ key='factory_job' and value='{job['id']}' }} and name='{job['id']}_{path.name}'"
        found = requests.get(base, headers=headers, params={"q": query, "fields": "files(id)", "supportsAllDrives": "true", "includeItemsFromAllDrives": "true"}, timeout=30)
        found.raise_for_status()
        matches = found.json().get("files", [])
        if matches:
            file_id = matches[0]["id"]
        else:
            mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            init = requests.post("https://www.googleapis.com/upload/drive/v3/files", params={"uploadType": "resumable", "supportsAllDrives": "true"}, headers={**headers, "X-Upload-Content-Type": mime}, json={"name": job["id"] + "_" + path.name, "parents": [parent], "appProperties": {"factory_job": job["id"]}}, timeout=30)
            init.raise_for_status()
            location = init.headers["Location"]
            from urllib.parse import urlparse
            parsed = urlparse(location)
            if parsed.scheme != "https" or parsed.hostname != "www.googleapis.com":
                raise ValueError("Unexpected Drive upload location")
            with open(path, "rb") as file:
                uploaded = requests.put(location, headers={**headers, "Content-Type": mime, "Content-Length": str(path.stat().st_size)}, data=file, timeout=600)
            uploaded.raise_for_status()
            file_id = uploaded.json()["id"]
        if path.name == "final.mp4":
            final_id = file_id
    store.update(job["id"], drive_id=final_id, error=None)
    return final_id

def deliver(job):
    """An ambiguous publish response stops for reconciliation; never blindly publish twice."""
    import requests
    from urllib.parse import urlparse
    url = os.environ.get("FACTORY_PUBLISH_WEBHOOK", "")
    secret = os.environ.get("FACTORY_PUBLISH_SECRET", "")
    if not url or not secret:
        raise ValueError("Configure the n8n publish webhook and secret first")
    if urlparse(url).scheme != "https":
        raise ValueError("Publishing webhook must use HTTPS")
    if not job["payload"]["destination"]:
        raise ValueError("Channel destination is empty")
    if digest(store.BASE / job["output"]) != job["approved_hash"]:
        raise ValueError("Approved video changed; publishing blocked")
    if not job["drive_id"]:
        raise ValueError("Upload the approved video to Drive first")
    store.transition(job["id"], "approved", "publishing")
    store.update(job["id"], delivery_attempted=1)
    try:
        response = requests.post(url, headers={"Authorization": "Bearer " + secret, "Idempotency-Key": job["id"]}, json={"job_id": job["id"], "drive_file_id": job["drive_id"], "destination": job["payload"]["destination"], "caption": job["payload"]["title"], "sha256": job["approved_hash"]}, timeout=90, allow_redirects=False)
        response.raise_for_status()
        receipt = response.json()
        if receipt.get("status") != "published" or not receipt.get("publish_id"):
            raise ValueError("Webhook must confirm published status and a publish_id")
        store.update(job["id"], status="published", publish_id=str(receipt["publish_id"])[:300], error=None)
    except Exception:
        store.update(job["id"], status="publish_unknown", error="Publishing response uncertain. Check platform/n8n execution before any retry; automatic retry disabled.")

def run_once():
    job = store.claim()
    if job:
        try:
            render(job)
        except Exception as exc:
            store.update(job["id"], status="failed", error=str(exc)[:1200])
        return True
    with store.connection() as db:
        ready = [store.unpack(row) for row in db.execute("SELECT * FROM jobs WHERE status IN ('awaiting_approval','approved') ORDER BY rowid")]
    for item in ready:
        if item["status"] not in ("awaiting_approval", "approved"):
            continue
        try:
            if not item["drive_id"] and integrations()["drive"]["configured"]:
                drive_upload(item)
                item = store.get_job(item["id"])
            if item["status"] == "approved" and integrations()["publisher"]["configured"]:
                deliver(item)
        except Exception:
            # Do not expose OAuth tokens or provider response bodies in public logs.
            store.update(item["id"], error="Delivery blocked. Check integration configuration and server logs; video remains saved locally.")
    return False

def loop():
    # flock/msvcrt lock prevents two API processes from rendering together.
    lock_file = open(store.DB.with_suffix(".worker.lock"), "a+")
    try:
        if os.name == "nt":
            import msvcrt
            lock_file.seek(0)
            lock_file.write("0")
            lock_file.flush()
            lock_file.seek(0)
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        lock_file.close()
        return
    try:
        with store.connection() as db:
            db.execute("UPDATE jobs SET status='failed', error='Worker restarted during rendering; inspect output, then retry' WHERE status='rendering'")
            db.execute("UPDATE jobs SET status='publish_unknown', error='Worker restarted during publishing; reconcile platform before retry' WHERE status='publishing'")
            db.execute("UPDATE jobs SET status='waiting_assets', error='Import interrupted; import the MP4 again' WHERE status='importing'")
        while not stop.is_set():
            try:
                busy = run_once()
            except Exception:
                busy = False
            stop.wait(1 if busy else 30)
    finally:
        lock_file.close()

def start():
    global worker
    with guard:
        if worker and worker.is_alive():
            return
        stop.clear()
        worker = threading.Thread(target=loop, daemon=True, name="factory-renderer")
        worker.start()
