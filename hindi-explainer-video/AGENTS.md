# AGENTS.md (for Codex) - Hindi explainer video project

Goal: produce 720x1280 / 30fps Hindi/Hinglish animated explainer MP4 with Remotion.

Workflow: follow `.agents/skills/hindi-explainer-video/SKILL.md` steps 1-7 and read its `references/` files.

Rules:
- TypeScript + Remotion only. Animate with useCurrentFrame/spring/interpolate, never CSS animation.
- Content lives in `data/script.json`; components are generic.
- Before coding: write script.md and a storyboard table, wait for approval.
- Run `npx tsc --noEmit` and render 1 still per scene before the final render.
- Commands: studio `npm run dev`; render `npx remotion render src/index.ts Main out/video.mp4`.
- Don't commit API keys; use `.env`.
- Codex strengths here: write/fix individual components and scenes; keep diffs small, one scene per task.
