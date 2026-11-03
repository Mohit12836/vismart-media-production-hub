# Vismart media production hub

Multi-channel, multi-recipe video production with a durable SQLite queue, isolated Remotion renders, technical checks, Drive delivery and approval-gated publishing.

The factory is a working production foundation, **not a guarantee of virality, 100 completed videos per day, free third-party services, or autonomous researched script writing**. Benchmark your actual VPS and confirm each provider connection before scaling.

## Run

Requires Python 3.10+, Node compatible with `hindi-reel/package.json`, FFmpeg/ffprobe, and Remotion's browser.

```sh
python -m pip install -r production_hub/requirements.txt
cd hindi-reel
npm install
npx remotion browser ensure
cd ../production_hub
python -m uvicorn web.app:app --host 127.0.0.1 --port 5000
```

Open `/`. An initial access key is created at `production_hub/runtime/admin.token` with owner-only permissions on Linux. Alternatively supply `FACTORY_ADMIN_TOKEN`. Keep it private. Use HTTPS or an SSH tunnel for remote access. Legacy UI is `/studio`; its old unsafe bulk renderer is disabled.

## Production workflow

1. Create channels in the dashboard: name, language label, brand colour and upload account reference.
2. Create separate automations for each channel/recipe: format, voice and daily cap.
3. Send **complete original scripts**, one scene per line, separated by `---` between videos; or submit JSON batches through `POST /api/factory/jobs` with a Bearer access key. Topic research and script generation belong in your upstream editorial/n8n/Hermes workflow; a topic alone is not a finished script.
4. Native recipes render automatically. External recipes wait for the edited MP4 import; no silent fallback to the same default video.
5. Review MP4 and cover. Technical QA checks H.264, dimensions, duration, audio presence and file hash. It does not certify factual accuracy, aesthetics, stock rights, or virality.
6. Drive receives video, cover, script, caption and manifest once configured. Approval is bound to the checked video hash. Publishing runs only after explicit approval, Drive upload, a configured destination and publisher credentials.

Each job has a separate directory and voice file. Restart during render marks the job failed for review/manual retry. Uncertain publish responses become `publish_unknown`; never blindly retry them. Duplicate normalized copy is blocked per channel, across recipes. Native starts are limited globally (default 100/day) and per automation, by Asia/Kolkata calendar day; failed attempts also count. One worker process owns an OS lock. The default single renderer fits a small shared VPS; throughput depends on duration/scene complexity.

## Recipes

| Recipe | Available path |
| --- | --- |
| Kinetic captions | Native scene-based text animation |
| Tips/listicle | Native numbered text layout |
| Quiz | Question, clues, final answer reveal |
| Storytelling | Native story beats; optional TTS |
| Photo story | Supplied images with slow motion + text |
| Canva template | Import a Canva-exported MP4 |
| Flow cinematic | Import an edited Flow MP4 |
| Screen demo | Import an edited screen-recorded MP4 |

Reels/stories are 1080×1920; landscape videos 1920×1080. Native landscape plans support 31–900 seconds. Voice must fit the requested duration; overlong audio fails explicitly rather than being truncated. Scenes currently share time evenly; word-timed captions, beat matching, automatic stock discovery, music selection, intelligent script generation and platform analytics are not implemented.

For photo stories, place images in `hindi-reel/public/factory-assets/` and supply one filename per scene in `assets`. Only local PNG/JPG/WEBP filenames are accepted. External edited MP4s are imported with `PUT /api/factory/jobs/{id}/source` (raw MP4, max 200 MB) and must match the format/duration plan. This is an actual import boundary, not unattended provider generation.

## Drive and publishing

Configure these in the **service environment**, never source control:

```text
FACTORY_ADMIN_TOKEN=private-access-key
FACTORY_DAILY_LIMIT=100
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REFRESH_TOKEN=your-authorized-refresh-token
GOOGLE_DRIVE_FOLDER_ID=your-private-folder-id
FACTORY_PUBLISH_WEBHOOK=https://your-n8n-host/webhook/approved-media
FACTORY_PUBLISH_SECRET=private-shared-secret
```

Google OAuth must grant Drive access to the destination folder. Files use job IDs and Drive `appProperties` for resumable/deduplicated delivery. A configured badge only indicates credentials exist; the first real request verifies provider access. Packages are saved in the configured Drive folder with job-prefixed filenames. Secrets/tokens are never returned by the state API.

The publisher webhook receives Bearer authorization plus `Idempotency-Key: <job_id>` and JSON:

```json
{"job_id":"...","drive_file_id":"...","destination":"account-ref","caption":"...","sha256":"..."}
```

Your n8n workflow must validate the secret, persist idempotency **before** platform side effects, download the private Drive file with its authorized Drive connection, select the configured account, upload via the platform's supported API, and reply only after confirmation:

```json
{"status":"published","publish_id":"actual-platform-post-id"}
```

An accepted/queued response is not treated as published. Platform credentials and approved account connections are required; this repo does not invent them. Reconcile a `publish_unknown` job against n8n/platform evidence before operator intervention. No automatic resubmission is provided.

Canva MCP in the chat and an unattended VPS integration have separate authorization. Free editor templates do not imply free autofill/API automation. Canva autofill depends on the eligible plan and template data fields: [official guide](https://www.canva.dev/docs/apps/rest-apis/autofill-guide/). Canva/Flow generation is not automatically called by this release. Local code templates work without those services.

## Validation

```sh
python -m pip install -r production_hub/requirements-test.txt
python -m unittest discover -s production_hub/tests -v
cd hindi-reel
npx tsc --noEmit
```

Tests cover simultaneous submissions, atomic batches, cross-recipe duplicate detection, daily claim quotas, approval/hash checks, uncertain publish handling, path validation and authenticated dashboard/API setup. Real renders and provider integration smoke tests must be recorded separately. Do not use the old system-wide `deploy_vps.sh` for incremental upgrades; it upgrades unrelated packages.
