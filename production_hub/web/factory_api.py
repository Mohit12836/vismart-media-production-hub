import hmac
import json
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from starlette.concurrency import run_in_threadpool
from pydantic import BaseModel, Field
from engine import factory_store as store, factory_runner as runner
from engine.recipes import RECIPES

router = APIRouter(prefix="/api/factory")

def expected_token():
    token = os.environ.get("FACTORY_ADMIN_TOKEN", "")
    token_file = store.BASE / "runtime" / "admin.token"
    if not token and token_file.exists():
        token = token_file.read_text().strip()
    return token

async def authorize(request: Request):
    expected = expected_token()
    supplied = request.headers.get("Authorization", "").removeprefix("Bearer ") or request.cookies.get("factory_session", "")
    if not expected or not hmac.compare_digest(supplied, expected):
        raise HTTPException(401, "Enter your factory access key")
    if request.method not in ("GET", "HEAD") and request.headers.get("Origin"):
        from urllib.parse import urlsplit
        if urlsplit(request.headers["Origin"]).netloc != request.headers.get("Host"):
            raise HTTPException(403, "Cross-site action blocked")

@router.post("/session")
async def session(request: Request):
    await authorize(request)
    response = JSONResponse({"status": "connected"})
    response.set_cookie("factory_session", expected_token(), httponly=True, samesite="strict", secure=request.url.scheme == "https", max_age=28800)
    return response

@router.get("/state")
async def state(request: Request):
    await authorize(request)
    return {"channels": store.list_rows("channels"), "automations": store.list_rows("automations"), "jobs": store.list_rows("jobs"),
            "recipes": RECIPES, "integrations": runner.integrations(), "daily_limit": int(os.environ.get("FACTORY_DAILY_LIMIT", "100")),
            "worker": bool(runner.worker and runner.worker.is_alive()), "enabled": store.enabled(), "timezone": "Asia/Kolkata",
            "creative_skills": json.loads((store.BASE/'creative_skills.json').read_text(encoding='utf8'))['sources']}

@router.get('/creative/examples')
async def creative_examples(request: Request):
    await authorize(request)
    return json.loads((store.BASE/'examples/creative-comparison.json').read_text(encoding='utf8'))

@router.post("/control/{action}")
async def control(action: str, request: Request):
    await authorize(request)
    if action not in ("pause", "resume"):
        raise HTTPException(422, "Choose pause or resume")
    store.enabled(action == "resume")
    runner.start()
    return {"enabled": store.enabled()}

@router.post("/channels")
async def channel(request: Request):
    await authorize(request)
    try:
        return {"id": store.channel(await request.json())}
    except (ValueError, TypeError) as exc:
        raise HTTPException(422, str(exc))

@router.post("/automations")
async def automation(request: Request):
    await authorize(request)
    try:
        return {"id": store.automation(await request.json())}
    except (ValueError, TypeError) as exc:
        raise HTTPException(422, str(exc))

@router.put("/channels/{item_id}")
async def edit_channel(item_id: str, request: Request):
    await authorize(request)
    try:
        return {"id": store.channel(await request.json(), item_id)}
    except (ValueError, TypeError) as exc:
        raise HTTPException(422, str(exc))

@router.put("/automations/{item_id}")
async def edit_automation(item_id: str, request: Request):
    await authorize(request)
    try:
        return {"id": store.automation(await request.json(), item_id)}
    except (ValueError, TypeError) as exc:
        raise HTTPException(422, str(exc))

class Batch(BaseModel):
    automation_id: str
    items: list[dict] = Field(min_length=1, max_length=100)

@router.post("/jobs")
async def submit(body: Batch, request: Request):
    await authorize(request)
    try:
        result = store.submit(body.automation_id, body.items)
        runner.start()
        return result
    except (ValueError, TypeError) as exc:
        raise HTTPException(422, str(exc))

@router.post("/jobs/{job_id}/{action}")
async def action(job_id: str, action: str, request: Request):
    await authorize(request)
    try:
        job = store.get_job(job_id)
        if action == "approve":
            runner.approve(job_id)
        elif action == "reject":
            store.transition(job_id, "awaiting_approval", "rejected")
        elif action == "retry":
            store.transition(job_id, "failed", "pending", error=None)
        else:
            raise ValueError("Unknown action")
        runner.start()
        return {"status": store.get_job(job["id"])["status"]}
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(409, str(exc))

@router.put("/jobs/{job_id}/source")
async def import_source(job_id: str, request: Request):
    await authorize(request)
    try:
        job = store.get_job(job_id)
        store.transition(job_id, "waiting_assets", "importing")
    except ValueError as exc:
        raise HTTPException(409, str(exc))
    folder = runner.OUTPUTS / job["channel_id"] / job_id
    folder.mkdir(parents=True, exist_ok=True)
    temp = folder / "upload.part"
    final = folder / "final.mp4"
    try:
        size = 0
        with open(temp, "wb") as output:
            async for block in request.stream():
                size += len(block)
                if size > 200 * 1024 * 1024:
                    raise ValueError("Import limited to 200 MB")
                output.write(block)
        await run_in_threadpool(runner.qa, temp, job["payload"])
        temp.replace(final)
        await run_in_threadpool(runner.finish, job, final)
        return {"status": "awaiting_approval"}
    except Exception as exc:
        temp.unlink(missing_ok=True)
        store.update(job_id, status="waiting_assets", error="Import failed. Check dimensions, codec, duration and audio against the job plan.")
        raise HTTPException(422, "Import failed; use H.264 MP4 with matching dimensions, duration and audio") from exc

@router.get("/jobs/{job_id}/file/{filename}")
async def download(job_id: str, filename: str, request: Request):
    await authorize(request)
    if filename not in ("final.mp4", "cover.jpg", "caption.txt", "script.txt", "manifest.json", "render.log", "subtitles.srt", "words.json", "timing.json", "creative-plan.json"):
        raise HTTPException(404)
    try:
        job = store.get_job(job_id)
    except ValueError:
        raise HTTPException(404)
    path = runner.OUTPUTS / job["channel_id"] / job_id / filename
    if not path.is_file():
        raise HTTPException(404)
    return FileResponse(path)
