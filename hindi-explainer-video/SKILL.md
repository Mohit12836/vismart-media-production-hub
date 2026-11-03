---
name: hindi-explainer-video
description: Build a 9:16 Hindi/Hinglish animated explainer reel (like "Website banao ₹0 me") with Remotion - mascot, bold subtitles, scene cards, Hindi voiceover, word-highlight captions and MP4 render. Use whenever the user asks for an explainer reel, short educational video, "esi video banao", Instagram/Shorts video from a topic, or animated Hindi/Hinglish video made with code - even if they don't say "Remotion".
---

# Hindi Explainer Video (Remotion)

Reference video pattern: 720x1280, 30fps, ~150s, white background, one mascot at bottom-left,
big Hindi headline on top, one illustrated "card" in the middle, highlighted subtitle strip at the bottom.
One idea per scene. Analogy-driven teaching (e.g. Domain = pata/address, Hosting = kamra/room).

Follow the steps IN ORDER. Do not write code before step 3 is approved.

## Step 1 - Brief (ask only what is missing)
Topic | Audience | Length (30/60/90/150s) | Language (Hindi / Hinglish) | Voice (male/female) | CTA (follow/save/share)

## Step 2 - Script (write in `script.md`)
Hook (0-5s, problem + promise) -> Analogy setup -> Concept 1 -> Concept 2 -> Options/Methods (numbered "tareeka 1/2/3")
-> Warnings ("bas 2 baatein") -> Recap -> CTA (share + save).
Rules:
- 1 sentence = 1 scene, max 12 words, 2-4 seconds.
- Use everyday analogy for each technical term (see references/teaching-patterns.md).
- Keywords in English inside Hindi sentence (Hinglish) - they become highlighted words.
- Add pattern interrupts every ~10s (question, "ruko!", surprise number).

## Step 3 - Storyboard table (get user approval)
| # | Time | Headline | Visual (card/illustration) | Subtitle line | Highlight words | Animation |
Include a progress "chip" label for each section (e.g. "tareeka 2").

## Step 4 - Project setup
```
npx create-video@latest hindi-reel --template blank
cd hindi-reel && npm i @remotion/transitions @remotion/captions @remotion/google-fonts zod
```
Structure: `src/Root.tsx`, `src/theme.ts`, `src/scenes/*.tsx`, `src/components/*.tsx`, `public/audio/`, `public/img/`, `data/script.json`.
Composition: width 720, height 1280, fps 30, durationInFrames computed from script.json.

## Step 5 - Build (read references as needed)
- Design tokens, fonts, colors -> references/design-system.md
- Reusable components (Mascot, Headline, Card, Chip, SubtitleBar, Sticker) -> references/components.md
- Voiceover + captions + sync -> references/voiceover-captions.md
- Teaching analogies / script patterns -> references/teaching-patterns.md

Hard rules:
1. All motion via `useCurrentFrame()` + `spring()`/`interpolate()`. NEVER CSS transitions/animations.
2. Data-driven: scenes come from `data/script.json`; no hardcoded text inside scene files.
3. Keep text inside safe zone: 60px side margins, top 120px and bottom 220px reserved for UI overlays.
4. Every scene has enter (0-10 frames) + hold + exit (last 6 frames) animation.
5. Scene length = voiceover audio length + 8 frames padding.
6. Only local assets (SVG/PNG). No remote URLs at render time.
7. Use `<Img>`, `<Audio>`, `<Sequence>`, `<TransitionSeries>` from Remotion, not plain tags.

## Step 6 - QA checklist
- `npx remotion still src/index.ts Main out/s01.png --frame=30` for each scene -> check text overflow
- Hindi glyphs render (font loaded with `loadFont` + subsets `devanagari`)
- Audio and subtitle highlight in sync (+-3 frames)
- No text outside safe zone, contrast ratio >= 4.5
- File size < 50MB: `npx remotion render src/index.ts Main out/video.mp4 --codec=h264 --crf=20`

## Step 7 - Deliver
Give MP4 path, duration, scene count, and ask for ONE round of feedback (script, visuals, speed).

## Claude vs Codex usage
- Claude Code: this folder at `.claude/skills/hindi-explainer-video/`. Invoke by asking "esi video banao: <topic>".
- Codex: put folder at `.agents/skills/hindi-explainer-video/` and add AGENTS.md from this bundle to the project root.
