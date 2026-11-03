---
name: vismart-unified-creative-director
description: Create Hindi/Hinglish/English explainers, sales ads, faceless stories and cinematic shorts with emotion-aware visual beat planning, 2D/3D style routing, word timing, code-first Remotion production, automated review and free-visual-only rules. Use for narration-driven videos, marketing reels, explainer shorts and video-story editing.
---
# Vismart Unified Creative Director — V1

## Mission
Understand *what the viewer must understand and feel* at each moment, then choose the simplest expressive full-frame treatment. Professional direction is not constant zoom, flash or a cut every second. Prioritize clarity, story causality, emotional restraint, mobile legibility, ethical claims and speed.

## Source inheritance
- Hindi Explainer: concise analogies, Devanagari typography, reusable cards, per-word captions, Remotion timing, mobile-safe areas.
- Faceless Shorts: six genre palettes/shot grammars (Deep Dive 3D, Night File 3D, Inside Out, Stick Story, Paper Atlas, Tall Tale 3D), flowing spoken sentences, narration-bound cuts, contact-sheet QA, code-first assets.
- Conflict resolution: **a sentence is NOT automatically a shot**. Plan semantic beats, then choose shot length 0.8–7+ s according to emotion; breaks are not mandatory. The source's default 1.5–3.5s is a *starting point* for energetic shorts only.
- The uploaded Faceless package contains README and SKILL rules, not its stated runnable style folders/three.js kit. Its styles are **design directions, not imported working implementations**. Original files are preserved in `references/original-*.md`.

## Zero-paid-visual policy
No paid image/video API, no subscriptions, no hidden credit spend. Render original SVG, procedural 2D, coded UI, reusable shapes/characters, locally licensed footage or free permitted stock. Never claim a photo/stock scene is real case proof. If 3D assets or an available GPU are absent, prefer 2D/2.5D instead of low-quality simulated 3D. Voice may be an externally provided paid file (e.g. ElevenLabs); all visuals and rendering must use free local tools subject to their applicable licenses. Check business-scale Remotion licensing separately.

## Production workflow (follow in order)
1. **Intent**: audience, outcome, language, channel, format, stakes, CTA, supplied footage, source facts. Infer sensible defaults; do not block simple briefs with repeated questions.
2. **Script**: write naturally spoken narrative; verify factual claims and annotate hypothetical metrics. Specify hook, curiosity, escalation, resolution, CTA. Don't add fabricated results.
3. **Emotion direction**: for each utterance, annotate intent, primary/subtle emotion, intensity 0–1, viewer emotion target, pause, emphasis, and confidence. Text-only interpretation is *hypothesis*; human/prosody review may revise it. Read `references/emotion-director.md`.
4. **Beat segmentation**: split on semantic reveals and voice emphasis, not every arbitrary second. For each beat define visual proposition, causal action, time range, shot, lens/frame, staging, foreground/background, motion, palette, audio cues and caption highlight. Use `references/scene-grammar.md`.
5. **Select renderer**: master = Remotion; SVG/React for UI, diagrams, 2D illustrations; Three/R3F optional for actual 3D; pre-rendered Blender/FFmpeg assets optional. Native `useCurrentFrame()` deterministic animation; never use independent wall-clock CSS animations in final export.
6. **Voice and timing**: use external approved voice or locally generated voice; align actual audio by word if timestamps available. Never pretend equal-duration word splitting is alignment; if forced alignment missing, mark captions `unverified` and review manually. Render silence intentionally and duck music under speech.
7. **Build**: create scene graph from JSON; preserve naming and versioning, cache assets by hash; render at 720×1280 draft / 1080×1920 final when hardware permits. Demo renderer included at `remotion/` is **2D baseline**, not full 3D.
8. **QA**: JSON schema and temporal checks; contact sheet every 0.5–1s plus boundaries; watch/listen to rendered video. Check legibility, captions, shot continuity, emotional appropriateness, claims, audio levels, held frames, dead air, cropping. Fix then rerender. `references/qa-contract.md`.
9. **Delivery**: MP4, cover frame, script, shot map, source/asset provenance and truthful QA summary. Do not claim tests passed without running them.

## Format contract
`scene-plan.json` has `meta` + `beats` with beat IDs, start/end seconds, `voice`, `emotion`, `viewer_goal`, `visual`, `shot`, `motion`, `caption`, `audio`, `asset_strategy`, `evidence`; see `examples/dentist-scene-plan.json`.

## Automation commands
- `python scripts/validate_plan.py examples/dentist-scene-plan.json`
- `python scripts/plan_from_script.py examples/dentist-script.txt > /tmp/draft-scene-plan.json` (heuristic first draft, **not definitive emotional understanding**)
- `cd remotion && npm install && npm run render:demo` (requires network once for package install; local rendering afterwards)

## Non-negotiable decision checks
- When worried voice: don't automatically darken or zoom; choose character/context/perception based on meaning.
- When surprised: reveal must land on stressed word, not one second late.
- When factual: evidence/diagram preferred over synthetic emotional footage.
- When product/UI demonstration: correct UI interactions preferred over invented photorealism.
- Don't imitate proprietary footage, creator frames, or unlicensed characters.
- No generic fixed mascot/card layout in every scene; use composition diversity without creating visual chaos.
